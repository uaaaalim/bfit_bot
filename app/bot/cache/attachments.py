class AttachmentsMemoryCache:
    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._items.get(key)

    def set(self, key: str, file_id: str) -> None:
        self._items[key] = file_id

    def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def load_many(self, items: dict[str, str]) -> None:
        self._items.update(items)