from __future__ import annotations

import asyncio
from datetime import timedelta

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.manager import ProviderManager
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.bootstrap.registrations.anthropic import (
    register_anthropic_provider,
)


async def main() -> None:
    registry = ProviderRegistry()
    factory = ProviderFactory()

    register_anthropic_provider(registry, factory)

    assert registry.exists(ProviderType.ANTHROPIC)
    assert factory.exists(ProviderType.ANTHROPIC)

    manager = ProviderManager(factory)
    config = ProviderConfig(
        provider_id="test",
        provider_type=ProviderType.ANTHROPIC,
        api_key="test-key",
        base_url="https://example.com",
        timeout=timedelta(seconds=5),
    )

    instance = await manager.add(config)
    assert instance.info.provider_type == ProviderType.ANTHROPIC
    assert manager.exists("test")

    await manager.close_all()
    assert not manager.exists("test")


def test_anthropic_minimal_provider_lifecycle() -> None:
    asyncio.run(main())
