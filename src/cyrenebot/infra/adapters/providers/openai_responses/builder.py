from cyrenebot.core.provider.provider_protocol import ProviderInstanceProtocol
from cyrenebot.core.schema.provider import ProviderConfig, ProviderInfo

from cyrenebot.infra.adapters.providers.openai_responses.instance import (
    OpenAIResponsesProviderInstance,
)


async def build_openai_responses_provider(
    config: ProviderConfig,
    info: ProviderInfo,
) -> ProviderInstanceProtocol:
    return OpenAIResponsesProviderInstance(
        config=config,
        info=info,
    )
