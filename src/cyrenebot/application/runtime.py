from __future__ import annotations

from dataclasses import dataclass

from cyrenebot.core.context.context_protocol import ContextBuilderProtocol
from cyrenebot.core.context.manager import ContextManager
from cyrenebot.core.provider.manager import ProviderManager
from cyrenebot.core.skill.manager import SkillManager
from cyrenebot.core.tool.manager import ToolManager
from cyrenebot.core.tool.tool_protocol import ToolRegistryProtocol


@dataclass(slots=True)
class CyreneBotRuntime:
    """
    CyreneBot 应用运行时
    """

    provider_manager: ProviderManager
    context_builder: ContextBuilderProtocol
    context_manager: ContextManager | None = None
    skill_manager: SkillManager | None = None
    tool_registry: ToolRegistryProtocol | None = None
    tool_manager: ToolManager | None = None
