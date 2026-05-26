from __future__ import annotations

import asyncio
import sys

import pytest

from cyreneAI.core.errors.tool import ToolExecutionError
from cyreneAI.core.schema.tool import ToolCall
from cyreneAI.infra.adapters.tools.subprocess.executor import SubprocessToolExecutor


async def _run_subprocess_tool() -> None:
    code = (
        "import json, sys; "
        "payload = json.load(sys.stdin); "
        "print(json.dumps({"
        "'content': 'value:' + payload['arguments']['key'], "
        "'metadata': {'tool': payload['name']}"
        "}))"
    )
    executor = SubprocessToolExecutor([sys.executable, "-c", code])
    result = await executor.execute(
        ToolCall(
            id="call-1",
            name="lookup",
            arguments="{\"key\":\"answer\"}",
        )
    )

    assert result.call_id == "call-1"
    assert result.name == "lookup"
    assert result.content == "value:answer"
    assert result.metadata == {"tool": "lookup"}


def test_subprocess_tool_executor_maps_json_stdout_result() -> None:
    asyncio.run(_run_subprocess_tool())


async def _run_failing_subprocess_tool() -> None:
    code = "import sys; print('boom', file=sys.stderr); sys.exit(2)"
    executor = SubprocessToolExecutor([sys.executable, "-c", code])
    await executor.execute(
        ToolCall(
            id="call-1",
            name="lookup",
            arguments="{}",
        )
    )


def test_subprocess_tool_executor_translates_nonzero_exit() -> None:
    with pytest.raises(ToolExecutionError):
        asyncio.run(_run_failing_subprocess_tool())
