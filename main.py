import logging

from src.initializing_creation import main


def setup_logger() -> logging.Logger:
    """Настраивает и возвращает логгер для приложения."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    logger = setup_logger()
    try:
        main()
    except Exception:
        logger.exception("Критическая ошибка при выполнении приложения")
