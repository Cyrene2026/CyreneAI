from __future__ import annotations

from cyreneAI.application.runtime import CyreneAIRuntime
from cyreneAI.core.context.builder import ContextWindowBuilder
from cyreneAI.core.context.context_protocol import (
    ContextBuilderProtocol,
    ContextStoreProtocol,
)
from cyreneAI.core.context.manager import ContextManager
from cyreneAI.core.provider.factory import ProviderFactory
from cyreneAI.core.provider.manager import ProviderManager
from cyreneAI.core.schema.provider import ProviderConfig
from cyreneAI.core.schema.skill import SkillDefinition
from cyreneAI.core.skill.manager import SkillManager
from cyreneAI.core.skill.registry import SkillRegistry
from cyreneAI.core.tool.manager import ToolManager
from cyreneAI.core.tool.registry import ToolRegistry
from cyreneAI.core.tool.tool_protocol import ToolRegistryProtocol
from cyreneAI.core.vector.manager import VectorManager
from cyreneAI.core.vector.vector_protocol import VectorStoreProtocol


async def build_cyrene_ai_runtime(
    *,
    provider_manager: ProviderManager | None = None,
    provider_factory: ProviderFactory | None = None,
    provider_configs: list[ProviderConfig] | None = None,
    context_builder: ContextBuilderProtocol | None = None,
    context_store: ContextStoreProtocol | None = None,
    skill_definitions: list[SkillDefinition] | None = None,
    tool_registry: ToolRegistryProtocol | None = None,
    vector_store: VectorStoreProtocol | None = None,
) -> CyreneAIRuntime:
    """
    从 core 对象和协议构建 CyreneAI 应用运行时。
    """
    runtime_provider_manager = provider_manager or ProviderManager(
        provider_factory or ProviderFactory()
    )

    for config in provider_configs or []:
        if config.enabled:
            await runtime_provider_manager.add(config)

    context_manager = None
    if context_store is not None:
        context_manager = ContextManager(context_store)

    skill_manager = None
    if skill_definitions is not None:
        skill_registry = SkillRegistry()
        for definition in skill_definitions:
            skill_registry.register(definition)
        skill_manager = SkillManager(skill_registry)

    runtime_tool_registry = tool_registry or ToolRegistry()
    return CyreneAIRuntime(
        provider_manager=runtime_provider_manager,
        context_builder=context_builder or ContextWindowBuilder(),
        context_manager=context_manager,
        vector_manager=(
            VectorManager(vector_store)
            if vector_store is not None
            else None
        ),
        skill_manager=skill_manager,
        tool_registry=runtime_tool_registry,
        tool_manager=ToolManager(runtime_tool_registry),
    )
