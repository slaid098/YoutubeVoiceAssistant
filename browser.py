from pathlib import Path

from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from loguru import logger


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


def get_url(url: str) -> None:
    try:
        driver.get(url)
    except WebDriverException as ex:
        logger.warning(f"{type(ex)} {ex}")
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")


driver = set_chrome_driver()
