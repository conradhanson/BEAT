from copy import copy

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from definitions import path_chromedriver
from definitions import path_geckodriver
from definitions import path_firefox_binary
from definitions import path_log_chrome
from definitions import path_log_firefox


def get_chrome(headless=True):
    """
    Define Chrome-specific options and return Chrome WebDriver instance

    Args:
        headless: bool

    Returns: WebDriver
        Chrome browser
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")  # OPEN BROWSER IN MAXIMIZED MODE
    chrome_options.add_argument("disable-infobars")  # DISABLING INFO BARS
    chrome_options.add_argument("--disable-extensions")  # DISABLING EXTENSIONS
    chrome_options.add_argument("--disable-dev-shm-usage")  # OVERCOME LIMITED RESOURCE PROBLEMS
    chrome_options.headless(headless)

    browser = webdriver.Chrome(chrome_options=chrome_options,
                               executable_path=path_chromedriver,
                               service_args=["--verbose", f"--log-path={path_log_chrome}"])
    browser.set_window_size(width=2560, height=1600)

    return browser


def get_firefox(headless=True):
    """
    Define Firefox-specific options and return Firefox WebDriver instance
    Args:
        headless: bool

    Returns: WebDriver
        Firefox browser
    """
    cap = copy(DesiredCapabilities).FIREFOX
    cap["marionette"] = headless

    browser = webdriver.Firefox(capabilities=cap,
                                firefox_binary=path_firefox_binary,
                                executable_path=path_geckodriver,
                                service_log_path=path_log_firefox,
                                timeout=15)
    browser.set_window_size(width=2560, height=1600)

    return browser
