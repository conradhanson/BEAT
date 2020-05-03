"""
LEAD GENERATION SCRIPT
"""
import csv
from time import time, sleep
from pyvirtualdisplay import Display

from crawler import Crawler
from definitions import ROOT_DIR


def script(state_code: str, subject: str):
    save_file = ROOT_DIR + 'businesses_' + state_code + '.csv'
    started = time()
    display = Display(visible=0, size=(2560, 1600), backend='xvfb')
    display.start()
    print('-> Starting Crawler')
    crawler = Crawler(headless=False)
    crawler.state_code = state_code

    # import cities of specified state_code
    with open(ROOT_DIR + '/cities.csv', 'r') as f:
        cities = []
        city_info = csv.reader(f)
        for city, state, _, _, _, _ in city_info:
            if state == state_code:
                cities.append(city)
        cities = set(cities)

    for city in cities:
        crawler.search_maps(city, state_code, subject, save_file)
        if crawler.page_count >= 25:
            sleep(60 * 60 * 4)  # SLEEP FOR 4 HRS AFTER COLLECTING 25 PAGES OF RESULTS
            crawler.page_count = 0

    crawler.quit()
    finished = time()
    display.stop()
    print((finished - started) / 3600)


if __name__ == '__main__':
    script(state_code='NC', subject='cafes')
