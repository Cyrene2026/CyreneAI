from __future__ import annotations

import asyncio
from pathlib import Path

from cyreneAI.core.schema.tool import ToolCall, ToolDefinition, ToolResult
from cyreneAI.core.tool.manager import ToolManager
from cyreneAI.core.tool.registry import ToolRegistry


class FakeToolExecutor:
    def __init__(self) -> None:
        self.calls: list[ToolCall] = []

    async def execute(self, call: ToolCall) -> ToolResult:
        self.calls.append(call)
        return ToolResult(
            call_id=call.id,
            name=call.name,
            content=f"executed:{call.arguments}",
        )


async def _run_tool_manager_execution() -> None:
    registry = ToolRegistry()
    executor = FakeToolExecutor()
    registry.register(
        ToolDefinition(
            name="lookup",
            description="Lookup a value.",
        ),
        executor,
    )
    manager = ToolManager(registry)
    call = ToolCall(
        id="call-1",
        name="lookup",
        arguments="{\"key\":\"value\"}",
    )

    result = await manager.execute(call)

    assert manager.exists("lookup")
    assert executor.calls == [call]
    assert result.call_id == "call-1"
    assert result.name == "lookup"
    assert result.content == "executed:{\"key\":\"value\"}"


def test_tool_manager_executes_registered_tool() -> None:
    asyncio.run(_run_tool_manager_execution())


def test_core_tools_does_not_import_infra_or_external_sdks() -> None:
    tools_dir = Path(__file__).parents[1] / "core" / "tool"
    forbidden_patterns = [
        "cyreneAI.infra",
        "openai",
        "anthropic",
        "google.genai",
        "httpx",
        "dotenv",
        "os.getenv",
    ]

    for path in tools_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            assert pattern not in text
