from __future__ import annotations

from cyreneAI.core.schema.tool import ToolResult


def test_tool_result_defaults_are_isolated() -> None:
    first = ToolResult(
        call_id="call-1",
        name="lookup",
        content="ok",
    )
    second = ToolResult(
        call_id="call-2",
        name="lookup",
    )

    first.metadata["key"] = "value"

    assert first.success is True
    assert first.error is None
    assert second.metadata == {}
