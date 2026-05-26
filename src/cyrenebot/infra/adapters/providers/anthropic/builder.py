from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.schema.provider import ProviderConfig, ProviderInfo
from cyrenebot.infra.adapters.providers.anthropic.instance import (
    AnthropicProviderInstance,
)


async def build_anthropic_provider(
    config: ProviderConfig,
    info: ProviderInfo,
) -> ProviderInstanceProtocol:
    return AnthropicProviderInstance(
        config=config,
        info=info,
    )
