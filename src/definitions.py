"""Definitions for project-wide use. Typically file paths."""
import os

# FILE PATHS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path_driver_firefox = '/usr/local/bin/geckodriver'  # LINUX
# path_driver_firefox = ROOT_DIR + '/configuration/geckodriver'  # WINDOWS
# path_driver_firefox = '/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver'  # MAC through HomeBrew
path_firefox_binary = '/usr/bin/firefox'
path_driver_chrome = 'usr/local/bin/chromedriver'  # LINUX
path_css_selectors = ROOT_DIR + '/css_selectors.json'
path_app_properties = ROOT_DIR + '/application.properties'
path_cities = ROOT_DIR + '/cities.csv'

# ROOT_SAVE_DIR = os.path.abspath('../') + '/results'  # LOCAL SAVE PATH
ROOT_SAVE_DIR = '/results'  # CONTAINER SAVE PATH
path_log_chrome = ROOT_SAVE_DIR + '/chrome.log'
path_log_firefox = ROOT_SAVE_DIR + '/firefox.log'
path_save_errors = ROOT_SAVE_DIR + '/errors/'
path_log = ROOT_SAVE_DIR + '/run.log'

# TIMEOUT DEFAULT
default_timeout = 60  # in seconds
