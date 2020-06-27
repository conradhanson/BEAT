from copy import copy
from pathlib import Path
import logging

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from selenium.webdriver import DesiredCapabilities

from definitions import ROOT_SAVE_DIR
from definitions import path_driver_chrome
from definitions import path_driver_firefox
from definitions import path_firefox_binary
from definitions import path_log_chrome
from definitions import path_log_firefox
from definitions import path_save_errors


class Browser(webdriver.Firefox):
    def __init__(self, width=2560, height=1600):
        cap = DesiredCapabilities.FIREFOX.copy()
        super(Browser, self).__init__(capabilities=cap,
                                      firefox_binary=path_firefox_binary,
                                      executable_path=path_driver_firefox,
                                      service_log_path=path_log_firefox)

        self.set_window_size(width, height)
        self.implicitly_wait(30)

    def get(self, url: str):
        """
        Wrapper for selenuium.webdriver.get to handle WebDriverException
        when "Failed to decode response from marionette"
        """
        try:
            super(Browser, self).get(url)
        except (WebDriverException, NoSuchWindowException) as e:
            if 'Message: Failed to decode response from marionette' in str(e) or \
               'Message: Browsing context has been discarded' in str(e):
                self.reset()
                logging.info('Marionette exception encountered. Resetting browser object.')
                self.get(url)
            else:
                logging.error(str(e))

    def reset(self):
        self.__init__()


def _get_chrome(width=2560, height=1600, headless=True):
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
    _init_chrome_log()
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


def _get_firefox(width=2560, height=1600):
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
    _init_firefox_log()
    cap = copy(DesiredCapabilities).FIREFOX

    browser = webdriver.Firefox(capabilities=cap,
                                firefox_binary=path_firefox_binary,
                                executable_path=path_driver_firefox,
                                service_log_path=path_log_firefox)
    browser.set_window_size(width, height)
    browser.implicitly_wait(30)

    return browser


def _init_firefox_log():
    # Make results and errors Dir
    if not Path(ROOT_SAVE_DIR).exists():
        Path(ROOT_SAVE_DIR).mkdir()
        Path(path_save_errors).mkdir()
    # Create / Clear Firefox Log
    if not Path(path_log_firefox).exists():
        with open(path_log_firefox, 'x') as f:
            f.write('\n')
    else:
        with open(path_log_firefox, 'w') as f:
            f.write('\n')


def _init_chrome_log():
    # Make results and errors Dir
    if not Path(ROOT_SAVE_DIR).exists():
        Path(ROOT_SAVE_DIR).mkdir()
        Path(path_save_errors).mkdir()
    # Create / Clear Chrome Log
    if not Path(path_log_chrome).exists():
        with open(path_log_chrome, 'x') as f:
            f.write('\n')
    else:
        with open(path_log_chrome, 'w') as f:
            f.write('\n')
