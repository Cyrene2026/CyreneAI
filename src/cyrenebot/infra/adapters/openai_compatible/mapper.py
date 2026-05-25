from cyrenebot.core.schema.chat import (
    ChatRequest,
    ChatResponse,
    ChatFinishReason,
)
from cyrenebot.core.schema.message import (
    MessageRole,
    ContentPartType,
    ContentPart,
    Message,
)

from openai.types import 


def map_chat_request_to_openai(request: ChatRequest) -> ChatRequest:
    """
    映射Chat请求到OpenAI格式
    """
