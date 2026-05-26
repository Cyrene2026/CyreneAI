from __future__ import annotations

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.adapters.providers.google_genai.builder import (
    build_google_genai_provider,
)
from cyrenebot.infra.provider_catalog.google_genai_info import (
    GOOGLE_GENAI_PROVIDER_INFO,
)


async def _build_google_genai_provider_with_info(
    config: ProviderConfig,
) -> ProviderInstanceProtocol:
    return await build_google_genai_provider(
        config=config,
        info=GOOGLE_GENAI_PROVIDER_INFO,
    )


def register_google_genai_provider(
    registry: ProviderRegistry,
    factory: ProviderFactory,
) -> None:
    registry.register_provider(GOOGLE_GENAI_PROVIDER_INFO)
    factory.register(
        ProviderType.GOOGLE,
        _build_google_genai_provider_with_info,
    )
