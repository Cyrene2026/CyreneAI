from __future__ import annotations

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.infra.bootstrap.registrations.anthropic import (
    register_anthropic_provider,
)
from cyrenebot.infra.bootstrap.registrations.google_genai import (
    register_google_genai_provider,
)
from cyrenebot.infra.bootstrap.registrations.openai_compatible import (
    register_openai_compatible_provider,
)
from cyrenebot.infra.bootstrap.registrations.openai_responses import (
    register_openai_responses_provider,
)


def register_default_providers(
    registry: ProviderRegistry,
    factory: ProviderFactory,
) -> None:
    """
    注册默认 provider
    """
    register_openai_compatible_provider(registry, factory)
    register_openai_responses_provider(registry, factory)
    register_anthropic_provider(registry, factory)
    register_google_genai_provider(registry, factory)
