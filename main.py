import atexit
import os

from loguru import logger

from command import do_commands
from exit import cleanup


def main() -> None:
    do_commands()


if __name__ == "__main__":
    try:
        atexit.register(cleanup)
        main()
    except KeyboardInterrupt:
        logger.info("Скрипт завершен")
        os._exit(1)
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")
        os._exit(1)
