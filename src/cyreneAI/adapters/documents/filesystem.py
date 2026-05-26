from __future__ import annotations

from pathlib import Path

from cyreneAI.core.schema.document import Document


class FileSystemDocumentLoader:
    """
    文件系统文档加载器。
    """

    def __init__(
        self,
        path: str | Path,
        *,
        extensions: set[str] | None = None,
        recursive: bool = True,
        encoding: str = "utf-8",
    ) -> None:
        self._path = Path(path)
        self._extensions = _normalize_extensions(extensions or {".md", ".txt"})
        self._recursive = recursive
        self._encoding = encoding

    def load(self) -> list[Document]:
        """
        加载支持的文本文件为 Document。
        """
        return [
            document
            for document in (
                self._load_file(path)
                for path in self._iter_files()
            )
            if document is not None
        ]

    def _iter_files(self) -> list[Path]:
        if self._path.is_file():
            return [self._path] if self._is_supported_file(self._path) else []

        if not self._path.exists():
            raise FileNotFoundError(f"Document path does not exist: {self._path}")
        if not self._path.is_dir():
            raise ValueError(f"Document path is not a file or directory: {self._path}")

        pattern = "**/*" if self._recursive else "*"
        return sorted(
            path
            for path in self._path.glob(pattern)
            if self._is_supported_file(path)
        )

    def _is_supported_file(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self._extensions

    def _load_file(self, path: Path) -> Document | None:
        content = path.read_text(encoding=self._encoding)
        if not content:
            return None

        relative_path = _relative_path(path=path, root=self._path)
        return Document(
            document_id=relative_path.as_posix(),
            content=content,
            metadata={
                "source": "filesystem",
                "path": path.as_posix(),
                "relative_path": relative_path.as_posix(),
                "filename": path.name,
                "extension": path.suffix.lower(),
            },
        )


def _normalize_extensions(extensions: set[str]) -> set[str]:
    return {
        extension.lower() if extension.startswith(".") else f".{extension.lower()}"
        for extension in extensions
    }


def _relative_path(*, path: Path, root: Path) -> Path:
    if root.is_file():
        return Path(path.name)
    try:
        return path.relative_to(root)
    except ValueError:
        return Path(path.name)
