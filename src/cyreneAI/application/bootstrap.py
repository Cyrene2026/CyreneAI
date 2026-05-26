from __future__ import annotations

from pathlib import Path

from cyreneAI.application.runtime import CyreneAIRuntime
from cyreneAI.core.context.builder import ContextWindowBuilder
from cyreneAI.core.context.context_protocol import ContextBuilderProtocol
from cyreneAI.core.context.manager import ContextManager
from cyreneAI.core.provider.factory import ProviderFactory
from cyreneAI.core.provider.manager import ProviderManager
from cyreneAI.core.provider.registry import ProviderRegistry
from cyreneAI.core.schema.provider import ProviderConfig
from cyreneAI.core.skill.manager import SkillManager
from cyreneAI.core.skill.registry import SkillRegistry
from cyreneAI.core.tool.manager import ToolManager
from cyreneAI.core.tool.registry import ToolRegistry
from cyreneAI.core.tool.tool_protocol import ToolRegistryProtocol
from cyreneAI.infra.adapters.skills.filesystem.loader import FileSystemSkillLoader
from cyreneAI.infra.bootstrap.registrations.providers import register_default_providers
from cyreneAI.infra.database.sqlite.builder import create_sqlite_context_store


async def build_cyrene_ai_runtime(
    *,
    provider_configs: list[ProviderConfig] | None = None,
    context_database_path: str | Path | None = None,
    skill_path: str | Path | None = None,
    context_builder: ContextBuilderProtocol | None = None,
    tool_registry: ToolRegistryProtocol | None = None,
) -> CyreneAIRuntime:
    """
    构建 CyreneAI 应用运行时
    """
    provider_registry = ProviderRegistry()
    provider_factory = ProviderFactory()
    register_default_providers(provider_registry, provider_factory)
    provider_manager = ProviderManager(provider_factory)

    for config in provider_configs or []:
        if config.enabled:
            await provider_manager.add(config)

    context_manager = None
    if context_database_path is not None:
        context_manager = ContextManager(
            await create_sqlite_context_store(context_database_path)
        )

    skill_manager = None
    if skill_path is not None:
        skill_registry = SkillRegistry()
        for definition in FileSystemSkillLoader(skill_path).load():
            skill_registry.register(definition)
        skill_manager = SkillManager(skill_registry)

    runtime_tool_registry = tool_registry or ToolRegistry()
    return CyreneAIRuntime(
        provider_manager=provider_manager,
        context_builder=context_builder or ContextWindowBuilder(),
        context_manager=context_manager,
        skill_manager=skill_manager,
        tool_registry=runtime_tool_registry,
        tool_manager=ToolManager(runtime_tool_registry),
    )
