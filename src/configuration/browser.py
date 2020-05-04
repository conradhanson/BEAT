from copy import copy

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from definitions import path_chromedriver
from definitions import path_geckodriver
from definitions import path_firefox_binary
from definitions import path_log_chrome
from definitions import path_log_firefox


def get_chrome(width=2560, height=1600, headless=True):
    """
    Define Chrome-specific options and return Chrome WebDriver instance

    Args:
        width: int
            of window
        height: int
            of window
        headless: bool

    Returns: WebDriver
        Chrome browser
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")  # OPEN BROWSER IN MAXIMIZED MODE
    chrome_options.add_argument("disable-infobars")  # DISABLING INFO BARS
    chrome_options.add_argument("--disable-extensions")  # DISABLING EXTENSIONS
    chrome_options.add_argument("--disable-dev-shm-usage")  # OVERCOME LIMITED RESOURCE PROBLEMS
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'window-size={width}x{height}')

    browser = webdriver.Chrome(chrome_options=chrome_options,
                               executable_path=path_chromedriver,
                               service_args=["--verbose", f"--log-path={path_log_chrome}"])
    browser.set_window_size(width, height)

    return browser


def get_firefox(width=2560, height=1600):
    """
    Define Firefox-specific options and return Firefox WebDriver instance

    Args:
        width: int
            of window
        height: int
            of window

    Returns: WebDriver
        Firefox browser
    """
    cap = copy(DesiredCapabilities).FIREFOX

    browser = webdriver.Firefox(capabilities=cap,
                                firefox_binary=path_firefox_binary,
                                executable_path=path_geckodriver,
                                service_log_path=path_log_firefox,
                                timeout=15)
    browser.set_window_size(width, height)

    return browser
