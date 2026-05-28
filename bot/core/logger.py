import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from colorama import Fore, Style, init

from bot.core import configuration


init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname

        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}[{record.levelname}]{Style.RESET_ALL}"

        message = super().format(record)

        record.levelname = original_levelname
        return message


class PlainFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname

        record.levelname = f"[{record.levelname}]"
        message = super().format(record)

        record.levelname = original_levelname
        return message


def get_folder_size(path: Path) -> int:
    if not path.exists():
        return 0

    return sum(file.stat().st_size for file in path.rglob("*") if file.is_file())


def cleanup_logs_folder(log_dir: Path, max_size_bytes: int) -> None:
    current_size = get_folder_size(log_dir)

    if current_size <= max_size_bytes:
        return

    log_files = sorted(
        log_dir.glob("*.log*"),
        key=lambda f: f.stat().st_mtime,
    )

    for file in log_files:
        if current_size <= max_size_bytes:
            break

        try:
            file_size = file.stat().st_size
            file.unlink()
            current_size -= file_size
        except OSError:
            pass


def setup_logging() -> None:
    log_dir = Path(configuration.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = getattr(logging, configuration.log_level.upper(), logging.INFO)

    file_max_bytes = configuration.log_file_max_mb * 1024 * 1024
    folder_max_bytes = configuration.log_folder_max_mb * 1024 * 1024

    cleanup_logs_folder(log_dir, folder_max_bytes)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"bot_{timestamp}.log"

    log_format = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    date_format = "%d-%m-%Y %H:%M:%S"

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    root_logger.handlers.clear()

    if configuration.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            ColoredFormatter(
                fmt=log_format,
                datefmt=date_format,
            )
        )
        root_logger.addHandler(console_handler)

    if configuration.log_to_file:
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=file_max_bytes,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(
            PlainFormatter(
                fmt=log_format,
                datefmt=date_format,
            )
        )
        root_logger.addHandler(file_handler)

    logging.getLogger(__name__).info("Logging initialized")