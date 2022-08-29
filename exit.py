from loguru import logger

from browser import driver


def cleanup():
    try:
        print("Выход")
        driver.close()
        driver.quit()
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")
