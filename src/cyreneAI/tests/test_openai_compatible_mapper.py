from __future__ import annotations

from openai.types.chat import ChatCompletion

from cyreneAI.core.schema.chat import ChatFinishReason, ChatRequest
from cyreneAI.core.schema.message import (
    ContentPart,
    ContentPartType,
    Message,
    MessageRole,
)
from cyreneAI.core.schema.tool import ToolChoice, ToolDefinition
from cyreneAI.infra.adapters.providers.openai_compatible.mapper import (
    map_chat_request,
    map_chat_response,
    map_finish_reason,
)


def test_map_chat_request_builds_openai_compatible_payload() -> None:
    request = ChatRequest(
        provider_id="provider-1",
        model="test-model",
        messages=[
            Message(
                role=MessageRole.USER,
                content=[
                    ContentPart(type=ContentPartType.TEXT, text="hello"),
                    ContentPart(type=ContentPartType.IMAGE, text="ignored"),
                ],
            )
        ],
        temperature=0,
        max_tokens=16,
        tools=[
            ToolDefinition(
                name="lookup",
                description="Lookup a value.",
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                    },
                },
            )
        ],
        tool_choice=ToolChoice(mode="tool", name="lookup"),
    )

    payload = map_chat_request(request)

    assert payload["model"] == "test-model"
    assert payload["messages"] == [
        {
            "role": "user",
            "content": "hello",
        }
    ]
    assert payload["temperature"] == 0
    assert payload["max_tokens"] == 16
    assert payload["stream"] is False
    assert payload["tools"] == [
        {
            "type": "function",
            "function": {
                "name": "lookup",
                "description": "Lookup a value.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                    },
                },
            },
        }
    ]
    assert payload["tool_choice"] == {
        "type": "function",
        "function": {
            "name": "lookup",
        },
    }
    assert "top_p" not in payload


def test_map_chat_response_builds_core_response() -> None:
    completion = ChatCompletion(
        id="chatcmpl-test",
        object="chat.completion",
        created=1,
        model="test-model",
        choices=[
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "pong",
                    "tool_calls": [
                        {
                            "id": "call-1",
                            "type": "function",
                            "function": {
                                "name": "lookup",
                                "arguments": "{\"key\":\"value\"}",
                            },
                        }
                    ],
                },
            }
        ],
        usage={
            "prompt_tokens": 3,
            "completion_tokens": 4,
            "total_tokens": 7,
        },
    )

    response = map_chat_response("provider-1", completion)

    assert response.provider_id == "provider-1"
    assert response.model == "test-model"
    assert response.finish_reason == ChatFinishReason.STOP
    assert response.usage is not None
    assert response.usage.prompt_tokens == 3
    assert response.usage.completion_tokens == 4
    assert response.usage.total_tokens == 7
    assert response.message is not None
    assert response.message.role == MessageRole.ASSISTANT
    assert response.message.content is not None
    assert response.message.content[0].text == "pong"
    assert response.tool_calls[0].id == "call-1"
    assert response.tool_calls[0].name == "lookup"
    assert response.tool_calls[0].arguments == "{\"key\":\"value\"}"


def test_map_finish_reason_handles_known_and_unknown_values() -> None:
    assert map_finish_reason("stop") == ChatFinishReason.STOP
    assert map_finish_reason("length") == ChatFinishReason.LENGTH
    assert map_finish_reason("tool_calls") == ChatFinishReason.TOOL_CALLS
    assert map_finish_reason("function_call") == ChatFinishReason.TOOL_CALLS
    assert map_finish_reason("content_filter") == ChatFinishReason.CONTENT_FILTER
    assert map_finish_reason("something-new") == ChatFinishReason.UNKNOWN
    assert map_finish_reason(None) == ChatFinishReason.UNKNOWN
