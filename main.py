import os

from loguru import logger

from command import do_commands
from browser import Driver


path_logs = "logs.log"

logger.add(path_logs, format="{time} {level} {message}",
           colorize=True, level="WARNING", rotation="1 MB", compression="zip")


def main() -> None:
    do_commands()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Скрипт завершен")
        os._exit(1)
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")
        os._exit(1)
    finally:
        if Driver.chrome is not None:
            Driver.chrome.close()
            Driver.chrome.quit()
