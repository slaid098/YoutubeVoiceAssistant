from loguru import logger

from browser import driver


def cleanup():
    try:
        driver.close()
        driver.quit()
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")
