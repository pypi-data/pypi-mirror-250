import ast
import hashlib
import logging
import os
import sys
import warnings
from enum import Enum
from functools import cache
from itertools import chain
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    no_type_check,
)

from httpx import Timeout
from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel
from rich import print

from langroid.cachedb.momento_cachedb import MomentoCache, MomentoCacheConfig
from langroid.cachedb.redis_cachedb import RedisCache, RedisCacheConfig
from langroid.language_models.base import (
    LanguageModel,
    LLMConfig,
    LLMFunctionCall,
    LLMFunctionSpec,
    LLMMessage,
    LLMResponse,
    LLMTokenUsage,
    Role,
)
from langroid.language_models.prompt_formatter.base import (
    PromptFormatter,
)
from langroid.language_models.utils import (
    async_retry_with_exponential_backoff,
    retry_with_exponential_backoff,
)
from langroid.utils.configuration import settings
from langroid.utils.constants import NO_ANSWER, Colors
from langroid.utils.system import friendly_error

logging.getLogger("openai").setLevel(logging.ERROR)


class OpenAIChatModel(str, Enum):
    """Enum for OpenAI Chat models"""

    GPT3_5_TURBO = "gpt-3.5-turbo-1106"
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-1106-preview"


class OpenAICompletionModel(str, Enum):
    """Enum for OpenAI Completion models"""

    TEXT_DA_VINCI_003 = "text-davinci-003"  # deprecated
    GPT3_5_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"


_context_length: Dict[str, int] = {
    # can add other non-openAI models here
    OpenAIChatModel.GPT3_5_TURBO: 4096,
    OpenAIChatModel.GPT4: 8192,
    OpenAIChatModel.GPT4_TURBO: 128_000,
    OpenAICompletionModel.TEXT_DA_VINCI_003: 4096,
}

_cost_per_1k_tokens: Dict[str, Tuple[float, float]] = {
    # can add other non-openAI models here.
    # model => (prompt cost, generation cost) in USD
    OpenAIChatModel.GPT3_5_TURBO: (0.0015, 0.002),
    OpenAIChatModel.GPT4: (0.03, 0.06),  # 8K context
    OpenAIChatModel.GPT4_TURBO: (0.01, 0.03),  # 128K context
}


openAIChatModelPreferenceList = [
    OpenAIChatModel.GPT4_TURBO,
    OpenAIChatModel.GPT4,
    OpenAIChatModel.GPT3_5_TURBO,
]

openAICompletionModelPreferenceList = [
    OpenAICompletionModel.GPT3_5_TURBO_INSTRUCT,
    OpenAICompletionModel.TEXT_DA_VINCI_003,
]


if "OPENAI_API_KEY" in os.environ:
    availableModels = set(map(lambda m: m.id, OpenAI().models.list()))
else:
    availableModels = set()

defaultOpenAIChatModel = next(
    chain(
        filter(
            lambda m: m.value in availableModels,
            openAIChatModelPreferenceList,
        ),
        [OpenAIChatModel.GPT4_TURBO],
    )
)
defaultOpenAICompletionModel = next(
    chain(
        filter(
            lambda m: m.value in availableModels,
            openAICompletionModelPreferenceList,
        ),
        [OpenAICompletionModel.GPT3_5_TURBO_INSTRUCT],
    )
)


class AccessWarning(Warning):
    pass


@cache
def gpt_3_5_warning() -> None:
    warnings.warn(
        """
        GPT-4 is not available, falling back to GPT-3.5.
        Examples may not work properly and unexpected behavior may occur.
        Adjustments to prompts may be necessary.
        """,
        AccessWarning,
    )


def noop() -> None:
    """Does nothing."""
    return None


class OpenAIGPTConfig(LLMConfig):
    """
    Class for any LLM with an OpenAI-like API: besides the OpenAI models this includes:
    (a) locally-served models behind an OpenAI-compatible API
    (b) non-local models, using a proxy adaptor lib like litellm that provides
        an OpenAI-compatible API.
    We could rename this class to OpenAILikeConfig.
    """

    type: str = "openai"
    api_key: str = ""  # CAUTION: set this ONLY via env var OPENAI_API_KEY
    organization: str = ""
    api_base: str | None = None  # used for local or other non-OpenAI models
    litellm: bool = False  # use litellm api?
    max_output_tokens: int = 1024
    min_output_tokens: int = 64
    use_chat_for_completion = True  # do not change this, for OpenAI models!
    timeout: int = 20
    temperature: float = 0.2
    seed: int | None = 42
    # these can be any model name that is served at an OpenAI-compatible API end point
    chat_model: str = defaultOpenAIChatModel
    completion_model: str = defaultOpenAICompletionModel
    run_on_first_use: Callable[[], None] = noop

    def __init__(self, **kwargs) -> None:  # type: ignore
        local_model = "api_base" in kwargs and kwargs["api_base"] is not None

        chat_model = kwargs.get("chat_model", "")
        if chat_model.startswith("litellm/") or chat_model.startswith("local/"):
            local_model = True

        warn_gpt_3_5 = (
            "chat_model" not in kwargs.keys()
            and not local_model
            and defaultOpenAIChatModel == OpenAIChatModel.GPT3_5_TURBO
        )

        if warn_gpt_3_5:
            existing_hook = kwargs.get("run_on_first_use", noop)

            def with_warning() -> None:
                existing_hook()
                gpt_3_5_warning()

            kwargs["run_on_first_use"] = with_warning

        super().__init__(**kwargs)

    # all of the vars above can be set via env vars,
    # by upper-casing the name and prefixing with OPENAI_, e.g.
    # OPENAI_MAX_OUTPUT_TOKENS=1000.
    # This is either done in the .env file, or via an explicit
    # `export OPENAI_MAX_OUTPUT_TOKENS=1000` or `setenv OPENAI_MAX_OUTPUT_TOKENS 1000`
    class Config:
        env_prefix = "OPENAI_"

    def _validate_litellm(self) -> None:
        """
        When using liteLLM, validate whether all env vars required by the model
        have been set.
        """
        if not self.litellm:
            return
        try:
            import litellm
        except ImportError:
            raise ImportError(
                """
                litellm not installed. Please install it via:
                pip install litellm.
                Or when installing langroid, install it with the `litellm` extra:
                pip install langroid[litellm]
                """
            )
        litellm.telemetry = False
        self.seed = None  # some local mdls don't support seed
        keys_dict = litellm.validate_environment(self.chat_model)
        missing_keys = keys_dict.get("missing_keys", [])
        if len(missing_keys) > 0:
            raise ValueError(
                f"""
                Missing environment variables for litellm-proxied model:
                {missing_keys}
                """
            )

    @classmethod
    def create(cls, prefix: str) -> Type["OpenAIGPTConfig"]:
        """Create a config class whose params can be set via a desired
        prefix from the .env file or env vars.
        E.g., using
        ```python
        OllamaConfig = OpenAIGPTConfig.create("ollama")
        ollama_config = OllamaConfig()
        ```
        you can have a group of params prefixed by "OLLAMA_", to be used
        with models served via `ollama`.
        This way, you can maintain several setting-groups in your .env file,
        one per model type.
        """

        class DynamicConfig(OpenAIGPTConfig):
            pass

        DynamicConfig.Config.env_prefix = prefix.upper() + "_"

        return DynamicConfig


class OpenAIResponse(BaseModel):
    """OpenAI response model, either completion or chat."""

    choices: List[Dict]  # type: ignore
    usage: Dict  # type: ignore


# Define a class for OpenAI GPT models that extends the base class
class OpenAIGPT(LanguageModel):
    """
    Class for OpenAI LLMs
    """

    def __init__(self, config: OpenAIGPTConfig = OpenAIGPTConfig()):
        """
        Args:
            config: configuration for openai-gpt model
        """
        super().__init__(config)
        self.config: OpenAIGPTConfig = config

        # Run the first time the model is used
        self.run_on_first_use = cache(self.config.run_on_first_use)

        # global override of chat_model,
        # to allow quick testing with other models
        if settings.chat_model != "":
            self.config.chat_model = settings.chat_model

        # if model name starts with "litellm",
        # set the actual model name by stripping the "litellm/" prefix
        # and set the litellm flag to True
        if self.config.chat_model.startswith("litellm/") or self.config.litellm:
            self.config.litellm = True
            self.api_base = self.config.api_base
            if self.config.chat_model.startswith("litellm/"):
                # strip the "litellm/" prefix
                self.config.chat_model = self.config.chat_model.split("/", 1)[1]
            # litellm/ollama/llama2 => ollama/llama2 for example
        elif self.config.chat_model.startswith("local/"):
            # expect this to be of the form "local/localhost:8000/v1",
            # depending on how the model is launched locally.
            # In this case the model served locally behind an OpenAI-compatible API
            # so we can just use `openai.*` methods directly,
            # and don't need a adaptor library like litellm
            self.config.litellm = False
            self.config.seed = None  # some models raise an error when seed is set
            # Extract the api_base from the model name after the "local/" prefix
            self.api_base = "http://" + self.config.chat_model.split("/", 1)[1]
        else:
            self.api_base = self.config.api_base

        # NOTE: The api_key should be set in the .env file, or via
        # an explicit `export OPENAI_API_KEY=xxx` or `setenv OPENAI_API_KEY xxx`
        # Pydantic's BaseSettings will automatically pick it up from the
        # .env file
        self.api_key = config.api_key or "xxx"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
            organization=self.config.organization,
            timeout=Timeout(self.config.timeout),
        )
        self.async_client = AsyncOpenAI(
            api_key=self.api_key,
            organization=self.config.organization,
            base_url=self.api_base,
            timeout=Timeout(self.config.timeout),
        )

        self.cache: MomentoCache | RedisCache
        if settings.cache_type == "momento":
            if config.cache_config is None or isinstance(
                config.cache_config, RedisCacheConfig
            ):
                # switch to fresh momento config if needed
                config.cache_config = MomentoCacheConfig()
            self.cache = MomentoCache(config.cache_config)
        elif "redis" in settings.cache_type:
            if config.cache_config is None or isinstance(
                config.cache_config, MomentoCacheConfig
            ):
                # switch to fresh redis config if needed
                config.cache_config = RedisCacheConfig(
                    fake="fake" in settings.cache_type
                )
            if "fake" in settings.cache_type:
                # force use of fake redis if global cache_type is "fakeredis"
                config.cache_config.fake = True
            self.cache = RedisCache(config.cache_config)
        else:
            raise ValueError(
                f"Invalid cache type {settings.cache_type}. "
                "Valid types are momento, redis, fakeredis"
            )

        self.config._validate_litellm()

    def is_openai_chat_model(self) -> bool:
        openai_chat_models = [e.value for e in OpenAIChatModel]
        return self.config.chat_model in openai_chat_models

    def _is_openai_completion_model(self) -> bool:
        openai_completion_models = [e.value for e in OpenAICompletionModel]
        return self.config.completion_model in openai_completion_models

    def chat_context_length(self) -> int:
        """
        Context-length for chat-completion models/endpoints
        Get it from the dict, otherwise fail-over to general method
        """
        model = (
            self.config.completion_model
            if self.config.use_completion_for_chat
            else self.config.chat_model
        )
        return _context_length.get(model, super().chat_context_length())

    def completion_context_length(self) -> int:
        """
        Context-length for completion models/endpoints
        Get it from the dict, otherwise fail-over to general method
        """
        model = (
            self.config.chat_model
            if self.config.use_chat_for_completion
            else self.config.completion_model
        )
        return _context_length.get(model, super().completion_context_length())

    def chat_cost(self) -> Tuple[float, float]:
        """
        (Prompt, Generation) cost per 1000 tokens, for chat-completion
        models/endpoints.
        Get it from the dict, otherwise fail-over to general method
        """
        return _cost_per_1k_tokens.get(self.config.chat_model, super().chat_cost())

    def set_stream(self, stream: bool) -> bool:
        """Enable or disable streaming output from API.
        Args:
            stream: enable streaming output from API
        Returns: previous value of stream
        """
        tmp = self.config.stream
        self.config.stream = stream
        return tmp

    def get_stream(self) -> bool:
        """Get streaming status"""
        return self.config.stream

    @no_type_check
    def _process_stream_event(
        self,
        event,
        chat: bool = False,
        has_function: bool = False,
        completion: str = "",
        function_args: str = "",
        function_name: str = "",
        is_async: bool = False,
    ) -> Tuple[bool, bool, str, str]:
        """Process state vars while processing a streaming API response.
            Returns a tuple consisting of:
        - is_break: whether to break out of the loop
        - has_function: whether the response contains a function_call
        - function_name: name of the function
        - function_args: args of the function
        """
        # convert event obj (of type ChatCompletionChunk) to dict so rest of code,
        # which expects dicts, works as it did before switching to openai v1.x
        if not isinstance(event, dict):
            event = event.model_dump()

        choices = event.get("choices", [{}])
        if len(choices) == 0:
            choices = [{}]
        event_args = ""
        event_fn_name = ""

        # The first two events in the stream of Azure OpenAI is useless.
        # In the 1st: choices list is empty, in the 2nd: the dict delta has null content
        if chat:
            delta = choices[0].get("delta", {})
            event_text = delta.get("content", "")
            if "function_call" in delta and delta["function_call"] is not None:
                if "name" in delta["function_call"]:
                    event_fn_name = delta["function_call"]["name"]
                if "arguments" in delta["function_call"]:
                    event_args = delta["function_call"]["arguments"]
        else:
            event_text = choices[0]["text"]
        if event_text:
            completion += event_text
            if not is_async:
                sys.stdout.write(Colors().GREEN + event_text)
                sys.stdout.flush()
        if event_fn_name:
            function_name = event_fn_name
            has_function = True
            if not is_async:
                sys.stdout.write(Colors().GREEN + "FUNC: " + event_fn_name + ": ")
                sys.stdout.flush()
        if event_args:
            function_args += event_args
            if not is_async:
                sys.stdout.write(Colors().GREEN + event_args)
                sys.stdout.flush()
        if choices[0].get("finish_reason", "") in ["stop", "function_call"]:
            # for function_call, finish_reason does not necessarily
            # contain "function_call" as mentioned in the docs.
            # So we check for "stop" or "function_call" here.
            return True, has_function, function_name, function_args, completion
        return False, has_function, function_name, function_args, completion

    @retry_with_exponential_backoff
    def _stream_response(  # type: ignore
        self, response, chat: bool = False
    ) -> Tuple[LLMResponse, Dict[str, Any]]:
        """
        Grab and print streaming response from API.
        Args:
            response: event-sequence emitted by API
            chat: whether in chat-mode (or else completion-mode)
        Returns:
            Tuple consisting of:
                LLMResponse object (with message, usage),
                Dict version of OpenAIResponse object (with choices, usage)

        """
        completion = ""
        function_args = ""
        function_name = ""

        sys.stdout.write(Colors().GREEN)
        sys.stdout.flush()
        has_function = False
        for event in response:
            (
                is_break,
                has_function,
                function_name,
                function_args,
                completion,
            ) = self._process_stream_event(
                event,
                chat=chat,
                has_function=has_function,
                completion=completion,
                function_args=function_args,
                function_name=function_name,
            )
            if is_break:
                break

        print("")
        # TODO- get usage info in stream mode (?)

        return self._create_stream_response(
            chat=chat,
            has_function=has_function,
            completion=completion,
            function_args=function_args,
            function_name=function_name,
            is_async=False,
        )

    @async_retry_with_exponential_backoff
    async def _stream_response_async(  # type: ignore
        self, response, chat: bool = False
    ) -> Tuple[LLMResponse, Dict[str, Any]]:
        """
        Grab and print streaming response from API.
        Args:
            response: event-sequence emitted by API
            chat: whether in chat-mode (or else completion-mode)
        Returns:
            Tuple consisting of:
                LLMResponse object (with message, usage),
                OpenAIResponse object (with choices, usage)

        """
        completion = ""
        function_args = ""
        function_name = ""

        sys.stdout.write(Colors().GREEN)
        sys.stdout.flush()
        has_function = False
        async for event in response:
            (
                is_break,
                has_function,
                function_name,
                function_args,
                completion,
            ) = self._process_stream_event(
                event,
                chat=chat,
                has_function=has_function,
                completion=completion,
                function_args=function_args,
                function_name=function_name,
            )
            if is_break:
                break

        print("")
        # TODO- get usage info in stream mode (?)

        return self._create_stream_response(
            chat=chat,
            has_function=has_function,
            completion=completion,
            function_args=function_args,
            function_name=function_name,
            is_async=True,
        )

    def _create_stream_response(
        self,
        chat: bool = False,
        has_function: bool = False,
        completion: str = "",
        function_args: str = "",
        function_name: str = "",
        is_async: bool = False,
    ) -> Tuple[LLMResponse, Dict[str, Any]]:
        # check if function_call args are valid, if not,
        # treat this as a normal msg, not a function call
        args = {}
        if has_function and function_args != "":
            try:
                args = ast.literal_eval(function_args.strip())
            except (SyntaxError, ValueError):
                logging.warning(
                    f"Parsing OpenAI function args failed: {function_args};"
                    " treating args as normal message"
                )
                has_function = False
                completion = completion + function_args

        # mock openai response so we can cache it
        if chat:
            msg: Dict[str, Any] = dict(message=dict(content=completion))
            if has_function:
                function_call = LLMFunctionCall(name=function_name)
                function_call_dict = function_call.dict()
                if function_args == "":
                    function_call.arguments = None
                else:
                    function_call.arguments = args
                    function_call_dict.update({"arguments": function_args.strip()})
                msg["message"]["function_call"] = function_call_dict
        else:
            # non-chat mode has no function_call
            msg = dict(text=completion)

        openai_response = OpenAIResponse(
            choices=[msg],
            usage=dict(total_tokens=0),
        )
        return (
            LLMResponse(
                message=completion,
                cached=False,
                function_call=function_call if has_function else None,
            ),
            openai_response.dict(),
        )

    def _cache_store(self, k: str, v: Any) -> None:
        self.cache.store(k, v)

    def _cache_lookup(self, fn_name: str, **kwargs: Dict[str, Any]) -> Tuple[str, Any]:
        # Use the kwargs as the cache key
        sorted_kwargs_str = str(sorted(kwargs.items()))
        raw_key = f"{fn_name}:{sorted_kwargs_str}"

        # Hash the key to a fixed length using SHA256
        hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()

        if not settings.cache:
            # when caching disabled, return the hashed_key and none result
            return hashed_key, None
        # Try to get the result from the cache
        return hashed_key, self.cache.retrieve(hashed_key)

    def _cost_chat_model(self, prompt: int, completion: int) -> float:
        price = self.chat_cost()
        return (price[0] * prompt + price[1] * completion) / 1000

    def _get_non_stream_token_usage(
        self, cached: bool, response: Dict[str, Any]
    ) -> LLMTokenUsage:
        """
        Extracts token usage from ``response`` and computes cost, only when NOT
        in streaming mode, since the LLM API (OpenAI currently) does not populate the
        usage fields in streaming mode. In streaming mode, these are set to zero for
        now, and will be updated later by the fn ``update_token_usage``.
        """
        cost = 0.0
        prompt_tokens = 0
        completion_tokens = 0
        if not cached and not self.get_stream():
            prompt_tokens = response["usage"]["prompt_tokens"]
            completion_tokens = response["usage"]["completion_tokens"]
            cost = self._cost_chat_model(
                response["usage"]["prompt_tokens"],
                response["usage"]["completion_tokens"],
            )

        return LLMTokenUsage(
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, cost=cost
        )

    def generate(self, prompt: str, max_tokens: int = 200) -> LLMResponse:
        self.run_on_first_use()

        try:
            return self._generate(prompt, max_tokens)
        except Exception as e:
            # capture exceptions not handled by retry, so we don't crash
            logging.error(friendly_error(e, "Error in OpenAIGPT.generate: "))
            return LLMResponse(message=NO_ANSWER, cached=False)

    def _generate(self, prompt: str, max_tokens: int) -> LLMResponse:
        if self.config.use_chat_for_completion:
            return self.chat(messages=prompt, max_tokens=max_tokens)

        if settings.debug:
            print(f"[red]PROMPT: {prompt}[/red]")

        @retry_with_exponential_backoff
        def completions_with_backoff(**kwargs):  # type: ignore
            cached = False
            hashed_key, result = self._cache_lookup("Completion", **kwargs)
            if result is not None:
                cached = True
                if settings.debug:
                    print("[red]CACHED[/red]")
            else:
                # If it's not in the cache, call the API
                result = self.client.completions.create(**kwargs)
                if self.get_stream():
                    llm_response, openai_response = self._stream_response(result)
                    self._cache_store(hashed_key, openai_response)
                    return cached, hashed_key, openai_response
                else:
                    self._cache_store(hashed_key, result.model_dump())
            return cached, hashed_key, result

        key_name = "model"
        cached, hashed_key, response = completions_with_backoff(
            **{key_name: self.config.completion_model},
            prompt=prompt,
            max_tokens=max_tokens,  # for output/completion
            temperature=self.config.temperature,
            echo=False,
            stream=self.get_stream(),
        )

        msg = response["choices"][0]["text"].strip()
        return LLMResponse(message=msg, cached=cached)

    async def agenerate(self, prompt: str, max_tokens: int = 200) -> LLMResponse:
        self.run_on_first_use()

        try:
            return await self._agenerate(prompt, max_tokens)
        except Exception as e:
            # capture exceptions not handled by retry, so we don't crash
            logging.error(friendly_error(e, "Error in OpenAIGPT.agenerate: "))
            return LLMResponse(message=NO_ANSWER, cached=False)

    async def _agenerate(self, prompt: str, max_tokens: int) -> LLMResponse:
        # note we typically will not have self.config.stream = True
        # when issuing several api calls concurrently/asynchronously.
        # The calling fn should use the context `with Streaming(..., False)` to
        # disable streaming.
        if self.config.use_chat_for_completion:
            messages = [
                LLMMessage(role=Role.SYSTEM, content="You are a helpful assistant."),
                LLMMessage(role=Role.USER, content=prompt),
            ]

            @async_retry_with_exponential_backoff
            async def completions_with_backoff(
                **kwargs: Dict[str, Any]
            ) -> Tuple[bool, str, Any]:
                cached = False
                hashed_key, result = self._cache_lookup("AsyncChatCompletion", **kwargs)
                if result is not None:
                    cached = True
                else:
                    if self.config.litellm:
                        from litellm import acompletion as litellm_acompletion
                    acompletion_call = (
                        litellm_acompletion
                        if self.config.litellm
                        else self.async_client.chat.completions.create
                    )

                    # If it's not in the cache, call the API
                    result = await acompletion_call(**kwargs)
                    self._cache_store(hashed_key, result.model_dump())
                return cached, hashed_key, result

            cached, hashed_key, response = await completions_with_backoff(
                model=self.config.chat_model,
                messages=[m.api_dict() for m in messages],
                max_tokens=max_tokens,
                temperature=self.config.temperature,
                stream=False,
            )
            if isinstance(response, dict):
                response_dict = response
            else:
                response_dict = response.model_dump()
            msg = response_dict["choices"][0]["message"]["content"].strip()
        else:
            # WARNING: .Completion.* endpoints are deprecated,
            # and as of Sep 2023 only legacy models will work here,
            # e.g. text-davinci-003, text-ada-001.
            @retry_with_exponential_backoff
            async def completions_with_backoff(**kwargs):  # type: ignore
                cached = False
                hashed_key, result = self._cache_lookup("AsyncCompletion", **kwargs)
                if result is not None:
                    cached = True
                else:
                    if self.config.litellm:
                        from litellm import acompletion as litellm_acompletion
                    acompletion_call = (
                        litellm_acompletion
                        if self.config.litellm
                        else self.async_client.completions.create
                    )
                    # If it's not in the cache, call the API
                    result = await acompletion_call(**kwargs)
                    self._cache_store(hashed_key, result.model_dump())
                return cached, hashed_key, result

            cached, hashed_key, response = await completions_with_backoff(
                model=self.config.completion_model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=self.config.temperature,
                echo=False,
                stream=False,
            )
            msg = response["choices"][0]["text"].strip()
        return LLMResponse(message=msg, cached=cached)

    def chat(
        self,
        messages: Union[str, List[LLMMessage]],
        max_tokens: int = 200,
        functions: Optional[List[LLMFunctionSpec]] = None,
        function_call: str | Dict[str, str] = "auto",
    ) -> LLMResponse:
        self.run_on_first_use()

        if functions is not None and not self.is_openai_chat_model():
            raise ValueError(
                f"""
                `functions` can only be specified for OpenAI chat models;
                {self.config.chat_model} does not support function-calling.
                Instead, please use Langroid's ToolMessages, which are equivalent.
                In the ChatAgentConfig, set `use_functions_api=False` 
                and `use_tools=True`, this will enable ToolMessages.
                """
            )
        if self.config.use_completion_for_chat and not self.is_openai_chat_model():
            # only makes sense for non-OpenAI models
            if self.config.formatter is None:
                raise ValueError(
                    """
                    `formatter` must be specified in config to use completion for chat.
                    """
                )
            formatter = PromptFormatter.create(self.config.formatter)
            if isinstance(messages, str):
                messages = [
                    LLMMessage(
                        role=Role.SYSTEM, content="You are a helpful assistant."
                    ),
                    LLMMessage(role=Role.USER, content=messages),
                ]
            prompt = formatter.format(messages)
            return self.generate(prompt=prompt, max_tokens=max_tokens)
        try:
            return self._chat(messages, max_tokens, functions, function_call)
        except Exception as e:
            # capture exceptions not handled by retry, so we don't crash
            logging.error(friendly_error(e, "Error in OpenAIGPT.chat: "))
            return LLMResponse(message=NO_ANSWER, cached=False)

    async def achat(
        self,
        messages: Union[str, List[LLMMessage]],
        max_tokens: int = 200,
        functions: Optional[List[LLMFunctionSpec]] = None,
        function_call: str | Dict[str, str] = "auto",
    ) -> LLMResponse:
        self.run_on_first_use()

        if functions is not None and not self.is_openai_chat_model():
            raise ValueError(
                f"""
                `functions` can only be specified for OpenAI chat models;
                {self.config.chat_model} does not support function-calling.
                Instead, please use Langroid's ToolMessages, which are equivalent.
                In the ChatAgentConfig, set `use_functions_api=False` 
                and `use_tools=True`, this will enable ToolMessages.
                """
            )
        # turn off streaming for async calls
        if self.config.use_completion_for_chat and not self.is_openai_chat_model():
            # only makes sense for local models
            if self.config.formatter is None:
                raise ValueError(
                    """
                    `formatter` must be specified in config to use completion for chat.
                    """
                )
            formatter = PromptFormatter.create(self.config.formatter)
            if isinstance(messages, str):
                messages = [
                    LLMMessage(
                        role=Role.SYSTEM, content="You are a helpful assistant."
                    ),
                    LLMMessage(role=Role.USER, content=messages),
                ]
            prompt = formatter.format(messages)
            return await self.agenerate(prompt=prompt, max_tokens=max_tokens)
        try:
            result = await self._achat(messages, max_tokens, functions, function_call)
            return result
        except Exception as e:
            # capture exceptions not handled by retry, so we don't crash
            logging.error(friendly_error(e, "Error in OpenAIGPT.achat: "))
            return LLMResponse(message=NO_ANSWER, cached=False)

    @retry_with_exponential_backoff
    def _chat_completions_with_backoff(self, **kwargs):  # type: ignore
        cached = False
        hashed_key, result = self._cache_lookup("Completion", **kwargs)
        if result is not None:
            cached = True
            if settings.debug:
                print("[red]CACHED[/red]")
        else:
            if self.config.litellm:
                from litellm import completion as litellm_completion
            # If it's not in the cache, call the API
            completion_call = (
                litellm_completion
                if self.config.litellm
                else self.client.chat.completions.create
            )
            result = completion_call(**kwargs)
            if not self.get_stream():
                # if streaming, cannot cache result
                # since it is a generator. Instead,
                # we hold on to the hashed_key and
                # cache the result later
                self._cache_store(hashed_key, result.model_dump())
        return cached, hashed_key, result

    @retry_with_exponential_backoff
    async def _achat_completions_with_backoff(self, **kwargs):  # type: ignore
        cached = False
        hashed_key, result = self._cache_lookup("Completion", **kwargs)
        if result is not None:
            cached = True
            if settings.debug:
                print("[red]CACHED[/red]")
        else:
            if self.config.litellm:
                from litellm import acompletion as litellm_acompletion
            acompletion_call = (
                litellm_acompletion
                if self.config.litellm
                else self.async_client.chat.completions.create
            )
            # If it's not in the cache, call the API
            result = await acompletion_call(**kwargs)
            if not self.get_stream():
                self._cache_store(hashed_key, result.model_dump())
        return cached, hashed_key, result

    def _prep_chat_completion(
        self,
        messages: Union[str, List[LLMMessage]],
        max_tokens: int,
        functions: Optional[List[LLMFunctionSpec]] = None,
        function_call: str | Dict[str, str] = "auto",
    ) -> Dict[str, Any]:
        if isinstance(messages, str):
            llm_messages = [
                LLMMessage(role=Role.SYSTEM, content="You are a helpful assistant."),
                LLMMessage(role=Role.USER, content=messages),
            ]
        else:
            llm_messages = messages

        # Azure uses different parameters. It uses ``engine`` instead of ``model``
        # and the value should be the deployment_name not ``self.config.chat_model``
        chat_model = self.config.chat_model
        key_name = "model"
        if self.config.type == "azure":
            if hasattr(self, "deployment_name"):
                chat_model = self.deployment_name

        args: Dict[str, Any] = dict(
            **{key_name: chat_model},
            messages=[m.api_dict() for m in llm_messages],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=self.config.temperature,
            stream=self.get_stream(),
        )
        if self.config.seed is not None:
            args.update(dict(seed=self.config.seed))
        # only include functions-related args if functions are provided
        # since the OpenAI API will throw an error if `functions` is None or []
        if functions is not None:
            args.update(
                dict(
                    functions=[f.dict() for f in functions],
                    function_call=function_call,
                )
            )
        return args

    def _process_chat_completion_response(
        self,
        cached: bool,
        response: Dict[str, Any],
    ) -> LLMResponse:
        # openAI response will look like this:
        """
        {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "name": "",
                    "content": "\n\nHello there, how may I help you?",
                    "function_call": {
                        "name": "fun_name",
                        "arguments: {
                            "arg1": "val1",
                            "arg2": "val2"
                        }
                    },
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }
        """
        message = response["choices"][0]["message"]
        msg = message["content"] or ""
        if message.get("function_call") is None:
            fun_call = None
        else:
            try:
                fun_call = LLMFunctionCall.from_dict(message["function_call"])
            except (ValueError, SyntaxError):
                logging.warning(
                    "Could not parse function arguments: "
                    f"{message['function_call']['arguments']} "
                    f"for function {message['function_call']['name']} "
                    "treating as normal non-function message"
                )
                fun_call = None
                args_str = message["function_call"]["arguments"] or ""
                msg_str = message["content"] or ""
                msg = msg_str + args_str

        return LLMResponse(
            message=msg.strip() if msg is not None else "",
            function_call=fun_call,
            cached=cached,
            usage=self._get_non_stream_token_usage(cached, response),
        )

    def _chat(
        self,
        messages: Union[str, List[LLMMessage]],
        max_tokens: int,
        functions: Optional[List[LLMFunctionSpec]] = None,
        function_call: str | Dict[str, str] = "auto",
    ) -> LLMResponse:
        """
        ChatCompletion API call to OpenAI.
        Args:
            messages: list of messages  to send to the API, typically
                represents back and forth dialogue between user and LLM, but could
                also include "function"-role messages. If messages is a string,
                it is assumed to be a user message.
            max_tokens: max output tokens to generate
            functions: list of LLMFunction specs available to the LLM, to possibly
                use in its response
            function_call: controls how the LLM uses `functions`:
                - "auto": LLM decides whether to use `functions` or not,
                - "none": LLM blocked from using any function
                - a dict of {"name": "function_name"} which forces the LLM to use
                    the specified function.
        Returns:
            LLMResponse object
        """
        args = self._prep_chat_completion(
            messages,
            max_tokens,
            functions,
            function_call,
        )
        cached, hashed_key, response = self._chat_completions_with_backoff(**args)
        if self.get_stream() and not cached:
            llm_response, openai_response = self._stream_response(response, chat=True)
            self._cache_store(hashed_key, openai_response)
            return llm_response  # type: ignore
        if isinstance(response, dict):
            response_dict = response
        else:
            response_dict = response.model_dump()
        return self._process_chat_completion_response(cached, response_dict)

    async def _achat(
        self,
        messages: Union[str, List[LLMMessage]],
        max_tokens: int,
        functions: Optional[List[LLMFunctionSpec]] = None,
        function_call: str | Dict[str, str] = "auto",
    ) -> LLMResponse:
        """
        Async version of _chat(). See that function for details.
        """
        args = self._prep_chat_completion(
            messages,
            max_tokens,
            functions,
            function_call,
        )
        cached, hashed_key, response = await self._achat_completions_with_backoff(
            **args
        )
        if self.get_stream() and not cached:
            llm_response, openai_response = await self._stream_response_async(
                response, chat=True
            )
            self._cache_store(hashed_key, openai_response)
            return llm_response  # type: ignore
        if isinstance(response, dict):
            response_dict = response
        else:
            response_dict = response.model_dump()
        return self._process_chat_completion_response(cached, response_dict)
