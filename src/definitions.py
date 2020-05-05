"""Definitions for project-wide use. Typically file paths."""
import os

# FILE PATHS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# path_geckodriver = ROOT_DIR + '/configuration/geckodriver'  # WINDOWS
path_geckodriver = '/usr/local/bin/geckodriver'  # LINUX
# path_geckodriver = '/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver'  # MAC through HomeBrew
path_firefox_binary = '/usr/bin/firefox'
path_chromedriver = ROOT_DIR + '/configuration/chromedriver'
path_css_selectors = ROOT_DIR + '/css_selectors.json'
path_app_properties = ROOT_DIR + '/application.properties'
path_cities = ROOT_DIR + '/cities.csv'

# SAVE PATHS
path_log_chrome = ROOT_DIR + '/results/chrome_log'
path_log_firefox = ROOT_DIR + '/results/firefox_log'
path_save_errors = ROOT_DIR + '/results/errors/'