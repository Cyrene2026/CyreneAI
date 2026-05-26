from __future__ import annotations

import pytest

from cyrenebot.core.errors.base import ConflictError
from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.provider import ProviderType
from cyrenebot.infra.bootstrap.registrations.providers import (
    register_default_providers,
)


def test_register_default_providers_registers_catalog_and_builders() -> None:
    registry = ProviderRegistry()
    factory = ProviderFactory()

    register_default_providers(registry, factory)

    assert registry.exists(ProviderType.OPENAI_COMPATIBLE)
    assert registry.exists(ProviderType.OPENAI_RESPONSES)
    assert registry.exists(ProviderType.ANTHROPIC)
    assert registry.exists(ProviderType.GOOGLE)
    assert factory.exists(ProviderType.OPENAI_COMPATIBLE)
    assert factory.exists(ProviderType.OPENAI_RESPONSES)
    assert factory.exists(ProviderType.ANTHROPIC)
    assert factory.exists(ProviderType.GOOGLE)


def test_register_default_providers_rejects_duplicate_registration() -> None:
    registry = ProviderRegistry()
    factory = ProviderFactory()

    register_default_providers(registry, factory)

    with pytest.raises(ConflictError):
        register_default_providers(registry, factory)
