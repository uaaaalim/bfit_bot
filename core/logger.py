import logging


def setup_logger(level: str = "INFO") -> logging.Logger:
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-6s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())

    return logging.getLogger("bfit_bot")
