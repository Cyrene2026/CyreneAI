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


class ChatProviderProtocol(ProviderInstanceProtocol, Protocol):
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        调用 provider 进行聊天
        """
        ...


class EmbeddingProviderProtocol(ProviderInstanceProtocol, Protocol):
    async def embed(self, text: str) -> list[float]:
        """
        调用 provider 进行文本嵌入
        """
        ...


class TTSProviderProtocol(ProviderInstanceProtocol, Protocol):
    async def tts(self, text: str) -> bytes:
        """
        调用 provider 进行文本转语音
        """
        ...
