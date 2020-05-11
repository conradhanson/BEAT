"""
LEAD GENERATION SCRIPT
"""
import argparse
import csv
import logging
from time import time, sleep

from pyvirtualdisplay import Display

from crawler import Crawler
from definitions import ROOT_SAVE_DIR
from definitions import path_cities
from definitions import path_log


def script(state_code: str, subject: str):
    started = time()
    window_size = (2560, 1600)
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

    for city in cities:
        logging.info(f'Searching {city}, {state_code}')
        path_save_file = ROOT_SAVE_DIR + f'/{city}_{state_code}_{subject}.csv'
        businesses = crawler.search_maps(city, state_code, subject)
        if businesses:
            with open(path_save_file, 'a', encoding='utf-8') as f:
                wr = csv.writer(f)
                wr.writerows(businesses)

        if crawler.page_count >= 25:
            sleep(60 * 60 * 4)  # SLEEP FOR 4 HRS AFTER COLLECTING 25 PAGES OF RESULTS
            crawler.page_count = 0

    crawler.quit()
    finished = time()
    display.stop()
    logging.info(f"Completed in {(finished - started) / 3600} hours.")


if __name__ == '__main__':
    # LOGGING CONFIGURATION
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.root.addHandler(logging.FileHandler(path_log, mode='w'))
    logging.root.addHandler(logging.StreamHandler())
    logging.getLogger("easyprocess").setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    # POSITIONAL ARGS
    parser.add_argument('subject', type=str,
                        help='the subject you want to search')
    parser.add_argument('state_code', type=str,
                        help='the two letter state abbreviation for where you want to search the subject')
    args = parser.parse_args()
    subject = args.subject.strip()
    state_code = args.state_code.strip().upper()

    if len(state_code) != 2:
        logging.error('State Code is invalid. Must be two letters.')
    elif not isinstance(state_code, str):
        logging.error('State Code is invalid. Must be a string.')
    elif not isinstance(subject, str):
        logging.error('Subject is invalid. Must be a string.')
    else:
        script(subject=args.subject, state_code=args.state_code)

    # script(state_code='NC', subject='cafes')
