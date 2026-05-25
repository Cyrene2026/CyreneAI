from openai import AsyncOpenAI
from cyrenebot.infra.adapters.openai_compatible.errors import (
    raise_openai_error,
)
from cyrenebot.infra.adapters.openai_compatible.mapper import (
    map_chat_request,
    map_chat_response,
    map_message,
    map_content_parts,
    map_tool,
    map_tools,
    map_tool_choice,
    map_chat_response,
    map_finish_reason,
    map_usage,
    map_tool_call,
)
from cyrenebot.core.schema.provider import (
    ProviderConfig,
    ProviderInfo,
)
from cyrenebot.core.errors.provider import ProviderConfigurationError
from cyrenebot.core.schema.chat import ChatRequest, ChatResponse


class OpenAICompatibleProviderInstance:
    def __init__(
        self,
        config: ProviderConfig,
        info: ProviderInfo,
    ) -> None:
        if not config.api_key:
            raise ProviderConfigurationError(
                "openai-compatible provider 必需提供api_key"
            )
        self.config = config
        self.info = info
        self.timeout = config.timeout.total_seconds() if config.timeout else None
        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=self.timeout,
        )

    async def close(self) -> None:
        await self._client.close()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            payload = map_chat_request(request)
            response = await self._client.chat.completions.create(**payload)
            return map_chat_response(
                provider_id=self.config.provider_id,
                response=response,
            )
        except Exception as exc:
            raise_openai_error(exc)
