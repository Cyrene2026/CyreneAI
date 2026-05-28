from __future__ import annotations

from pathlib import Path

from cyreneAI.application.bootstrap import (
    build_cyrene_ai_runtime as build_application_runtime,
)
from cyreneAI.application.runtime import CyreneAIRuntime
from cyreneAI.core.context.context_protocol import ContextBuilderProtocol
from cyreneAI.core.provider.factory import ProviderFactory
from cyreneAI.core.provider.registry import ProviderRegistry
from cyreneAI.core.schema.provider import ProviderConfig
from cyreneAI.core.tool.tool_protocol import ToolRegistryProtocol
from cyreneAI.core.vector.vector_protocol import VectorStoreProtocol
from cyreneAI.infra.adapters.skills.filesystem.loader import FileSystemSkillLoader
from cyreneAI.infra.adapters.vector_stores.sqlite.builder import (
    create_sqlite_vector_store,
)
from cyreneAI.infra.bootstrap.registrations.providers import register_default_providers
from cyreneAI.infra.database.sqlite.builder import create_sqlite_context_store


async def build_cyrene_ai_runtime(
    *,
    provider_configs: list[ProviderConfig] | None = None,
    context_database_path: str | Path | None = None,
    skill_path: str | Path | None = None,
    context_builder: ContextBuilderProtocol | None = None,
    tool_registry: ToolRegistryProtocol | None = None,
    vector_store: VectorStoreProtocol | None = None,
    vector_database_path: str | Path | None = None,
) -> CyreneAIRuntime:
    """
    构建带默认 infra 适配器的 CyreneAI 运行时。
    """
    provider_registry = ProviderRegistry()
    provider_factory = ProviderFactory()
    register_default_providers(provider_registry, provider_factory)

    context_store = None
    if context_database_path is not None:
        context_store = await create_sqlite_context_store(context_database_path)

    skill_definitions = None
    if skill_path is not None:
        skill_definitions = FileSystemSkillLoader(skill_path).load()

    runtime_vector_store = vector_store
    if runtime_vector_store is not None and vector_database_path is not None:
        raise ValueError("vector_store and vector_database_path cannot both be set")
    if runtime_vector_store is None and vector_database_path is not None:
        runtime_vector_store = await create_sqlite_vector_store(vector_database_path)

    return await build_application_runtime(
        provider_factory=provider_factory,
        provider_configs=provider_configs,
        context_builder=context_builder,
        context_store=context_store,
        skill_definitions=skill_definitions,
        tool_registry=tool_registry,
        vector_store=runtime_vector_store,
    )
