import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from colorama import Fore, Style, init


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
        original_name = record.name

        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL

        record.levelname = f"{color}{record.levelname}{reset}"
        record.name = f"{Fore.CYAN}{record.name}{reset}"

        formatted = super().format(record)

        record.levelname = original_levelname
        record.name = original_name

        return formatted


def setup_logging(
    log_dir: Path,
    level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 100,
) -> None:
    init(autoreset=True)

    log_dir.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"bot_{started_at}.log"

    file_format = (
        "%(asctime)s [%(levelname)s] %(name)s "
        "%(filename)s:%(lineno)d - %(message)s"
    )

    console_format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

    date_format = "%Y-%m-%d %H:%M:%S"

    file_formatter = logging.Formatter(
        fmt=file_format,
        datefmt=date_format,
    )

    console_formatter = ColoredFormatter(
        fmt=console_format,
        datefmt=date_format,
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[file_handler, console_handler],
        force=True,
    )

    logger = logging.getLogger(__name__)
    logger.info("Loaded logging, saving logs to '%s'", log_file)