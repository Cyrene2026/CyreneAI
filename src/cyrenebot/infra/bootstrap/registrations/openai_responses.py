from __future__ import annotations

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.adapters.providers.openai_responses.builder import (
    build_openai_responses_provider,
)
from cyrenebot.infra.provider_catalog.openai_responses_info import (
    OPENAI_RESPONSES_PROVIDER_INFO,
)


async def _build_openai_responses_provider_with_info(
    config: ProviderConfig,
) -> ProviderInstanceProtocol:
    return await build_openai_responses_provider(
        config=config,
        info=OPENAI_RESPONSES_PROVIDER_INFO,
    )


def register_openai_responses_provider(
    registry: ProviderRegistry,
    factory: ProviderFactory,
) -> None:
    registry.register_provider(OPENAI_RESPONSES_PROVIDER_INFO)
    factory.register(
        ProviderType.OPENAI_RESPONSES,
        _build_openai_responses_provider_with_info,
    )
