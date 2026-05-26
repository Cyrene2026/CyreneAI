from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.schema.provider import ProviderConfig, ProviderInfo
from cyrenebot.infra.adapters.providers.google_genai.instance import (
    GoogleGenAIProviderInstance,
)


async def build_google_genai_provider(
    config: ProviderConfig,
    info: ProviderInfo,
) -> ProviderInstanceProtocol:
    return GoogleGenAIProviderInstance(
        config=config,
        info=info,
    )
