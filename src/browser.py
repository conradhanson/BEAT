from copy import copy
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from definitions import ROOT_SAVE_DIR
from definitions import path_driver_chrome
from definitions import path_driver_firefox
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
    init_chrome_log()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")  # OPEN BROWSER IN MAXIMIZED MODE
    chrome_options.add_argument("disable-infobars")  # DISABLING INFO BARS
    chrome_options.add_argument("--disable-extensions")  # DISABLING EXTENSIONS
    chrome_options.add_argument("--disable-dev-shm-usage")  # OVERCOME LIMITED RESOURCE PROBLEMS
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'window-size={width}x{height}')

    browser = webdriver.Chrome(chrome_options=chrome_options,
                               executable_path=path_driver_chrome,
                               service_args=["--verbose", f"--log-path={path_log_chrome}"])
    browser.set_window_size(width, height)
    browser.implicitly_wait(30)

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
    init_firefox_log()
    cap = copy(DesiredCapabilities).FIREFOX

    browser = webdriver.Firefox(capabilities=cap,
                                firefox_binary=path_firefox_binary,
                                executable_path=path_driver_firefox,
                                service_log_path=path_log_firefox)
    browser.set_window_size(width, height)
    browser.implicitly_wait(30)

    return browser


def init_firefox_log():
    # Make Results Dir
    if not Path(ROOT_SAVE_DIR).exists():
        Path(ROOT_SAVE_DIR).mkdir()
    # Create / Clear Firefox Log
    if not Path(path_log_firefox).exists():
        with open(path_log_firefox, 'x') as f:
            f.write('\n')
    else:
        with open(path_log_firefox, 'w') as f:
            f.write('\n')


def init_chrome_log():
    # Make Results Dir
    if not Path(ROOT_SAVE_DIR).exists():
        Path(ROOT_SAVE_DIR).mkdir()
    # Create / Clear Chrome Log
    if not Path(path_log_chrome).exists():
        with open(path_log_chrome, 'x') as f:
            f.write('\n')
    else:
        with open(path_log_chrome, 'w') as f:
            f.write('\n')
