from __future__ import annotations

import asyncio
import json
from collections.abc import Sequence

from cyrenebot.core.errors.tool import ToolConfigurationError, ToolExecutionError
from cyrenebot.core.schema.tool import ToolCall, ToolResult
from cyrenebot.infra.adapters.tools.common import (
    make_tool_payload,
    map_json_text_tool_result,
    parse_tool_arguments,
)


class SubprocessToolExecutor:
    """
    子进程工具执行器
    """

    def __init__(
        self,
        command: Sequence[str],
        *,
        timeout: float = 30.0,
        cwd: str | None = None,
        environment: dict[str, str] | None = None,
    ) -> None:
        if not command:
            raise ToolConfigurationError("Subprocess tool command cannot be empty")

        self._command = tuple(command)
        self._timeout = timeout
        self._cwd = cwd
        self._environment = environment

    async def execute(self, call: ToolCall) -> ToolResult:
        """
        执行子进程工具
        """
        arguments = parse_tool_arguments(call.arguments)
        payload = make_tool_payload(call, arguments)
        input_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        process: asyncio.subprocess.Process | None = None

        try:
            process = await asyncio.create_subprocess_exec(
                *self._command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self._cwd,
                env=self._environment,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input_data),
                timeout=self._timeout,
            )
        except TimeoutError as exc:
            if process is not None:
                process.kill()
                await process.wait()
            raise ToolExecutionError(
                f"Tool {call.name} subprocess timed out",
                cause=exc,
            ) from exc
        except OSError as exc:
            raise ToolExecutionError(
                f"Tool {call.name} subprocess failed to start",
                cause=exc,
            ) from exc

        if process.returncode != 0:
            stderr_text = stderr.decode("utf-8", errors="replace").strip()
            raise ToolExecutionError(
                f"Tool {call.name} subprocess exited with "
                f"code {process.returncode}: {stderr_text}"
            )

        stdout_text = stdout.decode("utf-8", errors="replace")
        return map_json_text_tool_result(call, stdout_text)
