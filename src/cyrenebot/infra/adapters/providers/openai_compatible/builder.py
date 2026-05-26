from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.schema.provider import ProviderConfig, ProviderInfo

from cyrenebot.infra.adapters.providers.openai_compatible.instance import (
    OpenAICompatibleProviderInstance,
)


async def build_openai_compatible_provider(
    config: ProviderConfig,
    info: ProviderInfo,
) -> ProviderInstanceProtocol:
    return OpenAICompatibleProviderInstance(
        config=config,
        info=info,
    )
