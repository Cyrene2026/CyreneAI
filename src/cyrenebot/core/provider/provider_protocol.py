from typing import Protocol
from cyrenebot.core.schema.provider import ProviderInfo, ProviderConfig
from cyrenebot.core.schema.chat import ChatRequest, ChatResponse


class ProviderInstanceProtocol(Protocol):
    """
    provider 实例协议
    """

    info: ProviderInfo
    config: ProviderConfig

    async def close(self) -> None:
        """
        关闭 provider 实例
        """
        ...


class ProviderFactoryProtocol(Protocol):
    async def create(self, config: ProviderConfig) -> ProviderInstanceProtocol:
        """
        创建 provider 实例
        """
        ...


class ChatProviderProtocol(Protocol): ...


class EmbeddingProviderProtocol(Protocol): ...


class TTSProviderProtocol(Protocol): ...
