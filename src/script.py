""" BUSINESS EXTRACTION THROUGH AUTOMATION TOOL SCRIPT """
import argparse
import csv
import logging
from time import sleep
from time import time

from pyvirtualdisplay import Display

from crawler import Crawler
from definitions import ROOT_SAVE_DIR, max_timeout
from definitions import path_cities
from definitions import path_log


def script(state_code: str, subject: str, start_city: str = ''):
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

        businesses = crawler.search_subject(city, state_code, subject, page_limit=25, sleep_time=max_timeout)

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


if __name__ == '__main__':
    # LOGGING CONFIGURATION
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.root.addHandler(logging.FileHandler(path_log, mode='w', encoding='UTF-8'))
    logging.getLogger("easyprocess").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser()
    # POSITIONAL ARGS
    parser.add_argument('subject', type=str,
                        help='the subject you want to search')
    parser.add_argument('state_code', type=str,
                        help='the two letter state abbreviation for where you want to search the subject')
    parser.add_argument('-c', '--city', type=str,
                        help='the city you want to begin the search at (cities are searched alphabetically)')
    args = parser.parse_args()
    subject = args.subject.strip()
    state_code = args.state_code.strip().upper()

    if len(state_code) != 2:
        print(f"\"{state_code}\"")
        logging.error('State Code is invalid. Must be two letters.')
    elif not isinstance(state_code, str):
        logging.error('State Code is invalid. Must be a string.')
    elif not isinstance(subject, str):
        logging.error('Subject is invalid. Must be a string.')
    else:
        if args.city:
            city = args.city.strip()
            if not isinstance(city, str):
                logging.error('City is invalid. Must be a string.')
            else:
                script(subject=subject, state_code=state_code, start_city=city)
        else:
            script(subject=subject, state_code=state_code)
