import logging

logger = logging.getLogger(__name__)


class AttachmentsMemoryCache:
    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    def get(self, path: str) -> str | None:
        return self._items.get(path)

    def set(self, path: str, file_id: str) -> None:
        self._items[path] = file_id

    def delete(self, path: str) -> None:
        self._items.pop(path, None)

    def load_many(self, items: dict[str, str]) -> None:
        self._items.update(items)

    def clear(self) -> None:
        self._items.clear()