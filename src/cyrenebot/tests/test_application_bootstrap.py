from __future__ import annotations

import asyncio
import json

from cyrenebot.application.bootstrap import build_cyrenebot_runtime
from cyrenebot.core.schema.skill import SkillSelectionRequest
from cyrenebot.core.schema.tool import ToolCall, ToolDefinition, ToolResult


async def _run_build_runtime(tmp_path) -> None:
    skill_path = tmp_path / "skills.json"
    skill_path.write_text(
        json.dumps(
            [
                {
                    "name": "memory",
                    "description": "Use memory.",
                    "instructions": "Prefer relevant memory.",
                    "triggers": ["memory"],
                }
            ]
        ),
        encoding="utf-8",
    )

    runtime = await build_cyrenebot_runtime(
        context_database_path=tmp_path / "context.db",
        skill_path=skill_path,
    )

    assert runtime.context_manager is not None
    assert runtime.skill_manager is not None
    assert runtime.tool_registry is not None
    assert runtime.tool_manager is not None

    bundle = runtime.skill_manager.build_instruction_bundle(
        SkillSelectionRequest(text="Use memory.")
    )
    assert [instruction.name for instruction in bundle.instructions] == ["memory"]

    runtime.tool_registry.register(
        ToolDefinition(
            name="lookup",
            description="Lookup a value.",
        ),
        _FakeToolExecutor(),
    )
    result = await runtime.tool_manager.execute(
        _tool_call("call-1", "lookup", "{\"key\":\"value\"}")
    )
    assert result.content == "executed:{\"key\":\"value\"}"

    await runtime.context_manager.close()


class _FakeToolExecutor:
    async def execute(self, call) -> ToolResult:
        return ToolResult(
            call_id=call.id,
            name=call.name,
            content=f"executed:{call.arguments}",
        )


def _tool_call(call_id: str, name: str, arguments: str) -> ToolCall:
    return ToolCall(id=call_id, name=name, arguments=arguments)


def test_build_cyrenebot_runtime_wires_context_skills_and_tools(tmp_path) -> None:
    asyncio.run(_run_build_runtime(tmp_path))
