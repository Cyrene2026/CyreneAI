from __future__ import annotations

import asyncio
from datetime import timedelta

import pytest
from openai.types.chat import ChatCompletion

from cyrenebot.core.schema.chat import ChatFinishReason, ChatRequest
from cyrenebot.core.errors.provider import ProviderConfigurationError
from cyrenebot.core.schema.message import (
    ContentPart,
    ContentPartType,
    Message,
    MessageRole,
)
from cyrenebot.core.schema.provider import (
    ProviderCapability,
    ProviderConfig,
    ProviderInfo,
    ProviderType,
)
from cyrenebot.core.schema.tool import ToolChoice, ToolDefinition
from cyrenebot.infra.adapters.providers.openai_compatible.instance import (
    OpenAICompatibleProviderInstance,
)


def _provider_info() -> ProviderInfo:
    return ProviderInfo(
        provider_type=ProviderType.OPENAI_COMPATIBLE,
        name="OpenAI Compatible",
        description="test provider info",
        capabilities=[ProviderCapability.CHAT],
    )


class _FakeCompletions:
    def __init__(self, response: ChatCompletion) -> None:
        self.response = response
        self.payload = None

    async def create(self, **payload):
        self.payload = payload
        return self.response


class _FakeChat:
    def __init__(self, response: ChatCompletion) -> None:
        self.completions = _FakeCompletions(response)


class _FakeOpenAIClient:
    def __init__(self, response: ChatCompletion) -> None:
        self.chat = _FakeChat(response)
        self.closed = False

    async def close(self) -> None:
        self.closed = True


def test_openai_compatible_instance_requires_api_key() -> None:
    config = ProviderConfig(
        provider_id="test",
        provider_type=ProviderType.OPENAI_COMPATIBLE,
        api_key=None,
    )

    with pytest.raises(ProviderConfigurationError):
        OpenAICompatibleProviderInstance(
            config=config,
            info=_provider_info(),
        )


def test_openai_compatible_instance_converts_timeout_to_seconds() -> None:
    config = ProviderConfig(
        provider_id="test",
        provider_type=ProviderType.OPENAI_COMPATIBLE,
        api_key="test-key",
        timeout=timedelta(seconds=3),
    )

    instance = OpenAICompatibleProviderInstance(
        config=config,
        info=_provider_info(),
    )

    assert instance.timeout == 3
    asyncio.run(instance.close())


async def _run_chat_with_tool_call() -> None:
    completion = ChatCompletion(
        id="chatcmpl-test",
        object="chat.completion",
        created=1,
        model="test-model",
        choices=[
            {
                "index": 0,
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "content": None,
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
    )
    client = _FakeOpenAIClient(completion)
    config = ProviderConfig(
        provider_id="test",
        provider_type=ProviderType.OPENAI_COMPATIBLE,
        api_key="test-key",
        timeout=timedelta(seconds=3),
    )
    instance = OpenAICompatibleProviderInstance(
        config=config,
        info=_provider_info(),
        client=client,
    )
    request = ChatRequest(
        provider_id="test",
        model="test-model",
        messages=[
            Message(
                role=MessageRole.USER,
                content=[ContentPart(type=ContentPartType.TEXT, text="lookup it")],
            )
        ],
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

    response = await instance.chat(request)

    assert client.chat.completions.payload is not None
    assert client.chat.completions.payload["tools"] == [
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
    assert client.chat.completions.payload["tool_choice"] == {
        "type": "function",
        "function": {
            "name": "lookup",
        },
    }
    assert response.finish_reason == ChatFinishReason.TOOL_CALLS
    assert response.tool_calls[0].id == "call-1"
    assert response.tool_calls[0].name == "lookup"
    assert response.tool_calls[0].arguments == "{\"key\":\"value\"}"

    await instance.close()
    assert client.closed is True


def test_openai_compatible_instance_passes_tool_call_payload() -> None:
    asyncio.run(_run_chat_with_tool_call())
