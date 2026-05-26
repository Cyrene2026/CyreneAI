from __future__ import annotations

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.adapters.providers.anthropic.builder import (
    build_anthropic_provider,
)
from cyrenebot.infra.provider_catalog.anthropic_info import ANTHROPIC_PROVIDER_INFO


async def _build_anthropic_provider_with_info(
    config: ProviderConfig,
) -> ProviderInstanceProtocol:
    return await build_anthropic_provider(
        config=config,
        info=ANTHROPIC_PROVIDER_INFO,
    )


def register_anthropic_provider(
    registry: ProviderRegistry,
    factory: ProviderFactory,
) -> None:
    registry.register_provider(ANTHROPIC_PROVIDER_INFO)
    factory.register(
        ProviderType.ANTHROPIC,
        _build_anthropic_provider_with_info,
    )
