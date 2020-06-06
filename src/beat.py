import csv
import logging
from time import sleep
from time import time

from pyvirtualdisplay import Display

from crawler import Crawler
from definitions import ROOT_SAVE_DIR, max_timeout
from definitions import path_cities


def beat(state_code: str, subject: str, start_city: str = ''):
    """
    Business Extraction through Automation Tool
    Searches the subject in every city within a state alphabetically.

    Args:
        state_code: str
            to be searched
        subject: str
            to be searched
        start_city: str
            city to start the search at
    Returns:

    """
    # initialize virtual display, settings, and crawler
    started = time()
    window_size = (1920, 1080)
    display = Display(visible=False, size=window_size, backend='xvfb')
    display.start()
    logging.info('Starting Crawler')
    crawler = Crawler(width=window_size[0], height=window_size[1])
    crawler.state_code = state_code

    # import cities of specified state_code
    with open(path_cities, 'r') as f:
        cities = []
        city_info = csv.reader(f)
        for city, state, _, _, _, _ in city_info:
            if state == state_code:
                cities.append(city)
        cities = sorted(list(set(cities)))
        if start_city:
            try:
                cities = cities[cities.index(start_city):]
            except ValueError:
                logging.error(f"{start_city} does not exist in {state_code}")
                return

    # search each city of the state for the subject
    city_count = 0
    for city in cities:
        city_count += 1
        logging.info(f'Searching {city}, {state_code}')
        path_save_file = ROOT_SAVE_DIR + f'/{city}_{state_code}_{subject}.csv'

        businesses = crawler.search_subject(city, state_code, subject)

        if businesses:
            logging.info(f'Found {len(businesses)} contacts')
            with open(path_save_file, 'a', encoding='utf-8') as f:
                wr = csv.writer(f)
                wr.writerows(businesses)

        # AFTER SEARCHING # CITIES SLEEP FOR MAX TIMEOUT
        if city_count >= 3:
            city_count = 0
            logging.info(f"sleeping for {max_timeout / 3600} hrs")
            sleep(max_timeout)

    # cleanup
    crawler.quit()
    finished = time()
    display.stop()
    logging.info(f"Completed in {(finished - started) / 3600} hours.")
