from __future__ import annotations

import asyncio

import pytest

from cyrenebot.core.context.manager import ContextManager
from cyrenebot.core.errors.context import ContextNotFoundError
from cyrenebot.core.schema.context import ContextSnapshot, ContextWindow
from cyrenebot.infra.database.sqlite.builder import create_sqlite_context_store


def _snapshot(
    snapshot_id: str,
    session_id: str,
    *,
    value: str | None = None,
) -> ContextSnapshot:
    return ContextSnapshot(
        snapshot_id=snapshot_id,
        session_id=session_id,
        window=ContextWindow(
            window_id=f"{snapshot_id}:window",
            metadata={"value": value} if value is not None else {},
        ),
        metadata={"value": value} if value is not None else {},
    )


async def _run_store_lifecycle(database_path) -> None:
    store = await create_sqlite_context_store(database_path)
    try:
        first = _snapshot("snapshot-1", "session-1", value="first")
        second = _snapshot("snapshot-2", "session-1", value="second")
        other = _snapshot("snapshot-3", "session-2", value="other")

        await store.save_snapshot(first)
        await store.save_snapshot(second)
        await store.save_snapshot(other)

        assert await store.get_snapshot("snapshot-1") == first
        assert await store.list_snapshots("session-1") == [first, second]

        await store.delete_snapshot("snapshot-1")

        with pytest.raises(ContextNotFoundError):
            await store.get_snapshot("snapshot-1")
        assert await store.list_snapshots("session-1") == [second]
    finally:
        await store.close()


def test_sqlalchemy_context_store_persists_snapshot_lifecycle(tmp_path) -> None:
    asyncio.run(_run_store_lifecycle(tmp_path / "context.db"))


async def _run_store_overwrite(database_path) -> None:
    store = await create_sqlite_context_store(database_path)
    try:
        await store.save_snapshot(
            _snapshot("snapshot-1", "session-1", value="first")
        )
        latest = _snapshot("snapshot-1", "session-1", value="latest")
        await store.save_snapshot(latest)

        assert await store.get_snapshot("snapshot-1") == latest
        assert await store.list_snapshots("session-1") == [latest]
    finally:
        await store.close()


def test_sqlalchemy_context_store_overwrites_existing_snapshot(tmp_path) -> None:
    asyncio.run(_run_store_overwrite(tmp_path / "context.db"))


async def _run_context_manager_with_store(database_path) -> None:
    store = await create_sqlite_context_store(database_path)
    try:
        manager = ContextManager(store)
        snapshot = _snapshot("snapshot-1", "session-1", value="managed")

        await manager.save(snapshot)

        assert await manager.get("snapshot-1") == snapshot
        assert await manager.list_by_session("session-1") == [snapshot]

        await manager.remove("snapshot-1")

        with pytest.raises(ContextNotFoundError):
            await manager.get("snapshot-1")
    finally:
        await store.close()


def test_context_manager_works_with_sqlalchemy_context_store(tmp_path) -> None:
    asyncio.run(_run_context_manager_with_store(tmp_path / "context.db"))
