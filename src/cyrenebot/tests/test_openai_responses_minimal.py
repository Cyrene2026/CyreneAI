from __future__ import annotations

import asyncio
from datetime import timedelta

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.manager import ProviderManager
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.bootstrap.registrations.openai_responses import register_openai_responses_provider


async def main() -> None:
    registry = ProviderRegistry()
    factory = ProviderFactory()

    register_openai_responses_provider(registry, factory)

    assert registry.exists(ProviderType.OPENAI_RESPONSES)
    assert factory.exists(ProviderType.OPENAI_RESPONSES)

    manager = ProviderManager(factory)
    config = ProviderConfig(
        provider_id="test",
        provider_type=ProviderType.OPENAI_RESPONSES,
        api_key="test-key",
        base_url="https://example.com/v1",
        timeout=timedelta(seconds=5),
    )

    instance = await manager.add(config)
    assert instance.info.provider_type == ProviderType.OPENAI_RESPONSES
    assert manager.exists("test")

    await manager.close_all()
    assert not manager.exists("test")


def test_openai_responses_minimal_provider_lifecycle() -> None:
    asyncio.run(main())
