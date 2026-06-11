from aiogram.types import FSInputFile, Message

from attachments import PHOTO_PATHS

PHOTO_FILE_IDS: dict[int, dict[str, str]] = {}


def get_photo(bot_id: int, photo_key: str) -> str | FSInputFile:
    file_id = PHOTO_FILE_IDS.get(bot_id, {}).get(photo_key)
    if file_id:
        return file_id

    return FSInputFile(PHOTO_PATHS[photo_key])


def save_photo_id(bot_id: int, photo_key: str, message: Message | bool) -> None:
    if not isinstance(message, Message) or not message.photo:
        return

    PHOTO_FILE_IDS.setdefault(bot_id, {})[photo_key] = message.photo[-1].file_id
