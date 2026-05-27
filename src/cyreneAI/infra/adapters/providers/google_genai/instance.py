import asyncio
import math
from typing import Any

from google import genai
from google.genai import types

from cyreneAI.core.errors.provider import ProviderConfigurationError
from cyreneAI.core.schema.chat import ChatRequest, ChatResponse
from cyreneAI.core.schema.provider import ProviderConfig, ProviderInfo
from cyreneAI.infra.adapters.providers.google_genai.errors import (
    raise_google_genai_error,
)
from cyreneAI.infra.adapters.providers.google_genai.mapper import (
    map_google_genai_request,
    map_google_genai_response,
)


class GoogleGenAIProviderInstance:
    def __init__(
        self,
        config: ProviderConfig,
        info: ProviderInfo,
        client: Any | None = None,
    ) -> None:
        if not config.api_key:
            raise ProviderConfigurationError("google-genai provider 必需提供api_key")

        self.config = config
        self.info = info
        self.timeout = config.timeout.total_seconds() if config.timeout else None
        self._client = client or genai.Client(
            api_key=config.api_key,
            http_options=_build_http_options(config),
        )

    async def close(self) -> None:
        close = getattr(self._client, "close", None)
        if close is not None:
            result = close()
            if hasattr(result, "__await__"):
                await result

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            payload = map_google_genai_request(request)
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                **payload,
            )
            return map_google_genai_response(
                provider_id=self.config.provider_id,
                response=response,
            )
        except Exception as exc:
            raise_google_genai_error(exc)


def _build_http_options(config: ProviderConfig) -> types.HttpOptions | None:
    if config.base_url is None and config.timeout is None:
        return None
    return types.HttpOptions(
        base_url=config.base_url,
        timeout=(
            math.ceil(config.timeout.total_seconds())
            if config.timeout is not None
            else None
        ),
    )
