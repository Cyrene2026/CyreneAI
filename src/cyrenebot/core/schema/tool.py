from __future__ import annotations
from typing import Any, Literal
from pydantic import Field

from cyrenebot.core.schema.base import CyreneBotSchema


class ToolDefinition(CyreneBotSchema):
    """
    工具定义schema
    """

    name: str
    description: str
    parameters_schema: dict[str, Any] | None = None


class ToolCall(CyreneBotSchema):
    """
    工具调用schema
    """

    id: str
    name: str
    arguments: str | None = None


class ToolResult(CyreneBotSchema):
    """
    工具执行结果schema
    """

    call_id: str
    name: str
    content: str | None = None
    success: bool = True
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolChoice(CyreneBotSchema):
    """
    工具选择schema
    """

    mode: Literal["auto", "none", "required", "tool"] = "auto"
    name: str | None = None
