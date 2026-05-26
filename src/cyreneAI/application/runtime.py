from __future__ import annotations

from dataclasses import dataclass

from cyreneAI.core.context.context_protocol import ContextBuilderProtocol
from cyreneAI.core.context.manager import ContextManager
from cyreneAI.core.provider.manager import ProviderManager
from cyreneAI.core.skill.manager import SkillManager
from cyreneAI.core.tool.manager import ToolManager
from cyreneAI.core.tool.tool_protocol import ToolRegistryProtocol


@dataclass(slots=True)
class CyreneAIRuntime:
    """
    CyreneAI 应用运行时
    """

    provider_manager: ProviderManager
    context_builder: ContextBuilderProtocol
    context_manager: ContextManager | None = None
    skill_manager: SkillManager | None = None
    tool_registry: ToolRegistryProtocol | None = None
    tool_manager: ToolManager | None = None
