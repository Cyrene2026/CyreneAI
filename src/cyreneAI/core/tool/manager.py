from __future__ import annotations

from cyreneAI.core.schema.tool import ToolCall, ToolResult
from cyreneAI.core.tool.tool_protocol import ToolRegistryProtocol


class ToolManager:
    """
    工具运行管理器
    """

    def __init__(self, registry: ToolRegistryProtocol) -> None:
        self._registry = registry

    async def execute(self, call: ToolCall) -> ToolResult:
        """
        执行工具调用
        """
        executor = self._registry.get_executor(call.name)
        return await executor.execute(call)

    def exists(self, name: str) -> bool:
        """
        判断工具是否存在
        """
        return self._registry.exists(name)
