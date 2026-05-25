from __future__ import annotations

import asyncio
import os
from datetime import timedelta

import pytest
from dotenv import load_dotenv

from cyrenebot.core.provider.factory import ProviderFactory
from cyrenebot.core.provider.manager import ProviderManager
from cyrenebot.core.provider.registry import ProviderRegistry
from cyrenebot.core.schema.chat import ChatFinishReason, ChatRequest
from cyrenebot.core.schema.message import (
    ContentPart,
    ContentPartType,
    Message,
    MessageRole,
)
from cyrenebot.core.schema.provider import ProviderConfig, ProviderType
from cyrenebot.infra.bootstrap.openai_compatible import (
    register_openai_compatible_provider,
)


async def _run_real_chat() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_COMPATIBLE_MODEL") or os.getenv("OPENAI_MODEL")

    if not api_key:
        pytest.skip("OPENAI_COMPATIBLE_API_KEY or OPENAI_API_KEY is required")
    if not model:
        pytest.skip("OPENAI_COMPATIBLE_MODEL or OPENAI_MODEL is required")

    registry = ProviderRegistry()
    factory = ProviderFactory()
    register_openai_compatible_provider(registry, factory)

    manager = ProviderManager(factory)
    config = ProviderConfig(
        provider_id="real-openai-compatible",
        provider_type=ProviderType.OPENAI_COMPATIBLE,
        api_key=api_key,
        base_url=base_url,
        timeout=timedelta(seconds=30),
    )

    request = ChatRequest(
        provider_id=config.provider_id,
        model=model,
        messages=[
            Message(
                role=MessageRole.USER,
                content=[
                    ContentPart(
                        type=ContentPartType.TEXT,
                        text="Reply with exactly: Hello world!",
                    )
                ],
            )
        ],
        temperature=0,
        max_tokens=16,
    )

    try:
        instance = await manager.add(config)
        response = await instance.chat(request)

        assert response.provider_id == config.provider_id
        assert response.finish_reason in {
            ChatFinishReason.STOP,
            ChatFinishReason.LENGTH,
        }
        assert response.message is not None
        assert response.message.content is not None
        assert response.message.content[0].text

        print()
        print("openai-compatible real chat response:")
        print(f"  model: {response.model}")
        print(f"  finish_reason: {response.finish_reason}")
        print(f"  usage: {response.usage}")
        print(f"  text: {response.message.content[0].text}")
    finally:
        await manager.close_all()


def test_openai_compatible_real_chat() -> None:
    asyncio.run(_run_real_chat())
