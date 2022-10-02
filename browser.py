from pathlib import Path

from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from loguru import logger


def get_url(url: str = "") -> None:
    try:
        _close_driver()
        Driver.chrome = set_chrome_driver()
        _browser_to_front()
        _get_url(url)
    except WebDriverException as ex:
        logger.warning(f"{type(ex)} {ex}")
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")


def _close_driver() -> None:
    try:
        if Driver.chrome is not None:
            Driver.chrome.close()
            Driver.chrome.quit()
    except Exception:
        pass


def _browser_to_front() -> None:
    try:
        driver = Driver.chrome
        if driver is not None:
            driver.minimize_window()
            driver.maximize_window()
    except WebDriverException as ex:
        logger.warning(f"{type(ex)} {ex}")
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")


def _get_url(url: str) -> None:
    driver = Driver.chrome
    if driver is not None:
        if url != "":
            driver.get(url)


def set_chrome_driver() -> Chrome:
    path_webdriver = Path("driver")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("enable-automation")
    options.add_argument("--start-maximized")

    return webdriver.Chrome(service=Service(
        ChromeDriverManager(path=path_webdriver).install()), options=options)


class Driver:
    """
    stores an instance of the current browser
    """
    chrome: Chrome | None = None
