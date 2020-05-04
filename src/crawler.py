import json
import re
from time import sleep

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# MODULE
from configuration import browser
from definitions import path_css_selectors
from definitions import path_errors
from errors import custom_errors


class Crawler:
    def __init__(self, width=2560, height=1600, headless=True):
        """
        Crawl Google Maps for business info

        Args:
            headless: bool
        """
        with open(path_css_selectors, 'r') as f:
            self.css_selectors = json.load(f)

        self.browser = browser.get_firefox(width=width, height=height)
        # self.browser = browser.get_chrome(width=width, height=height, headless=headless)
        self.page_count = 0

    def quit(self):
        if self.browser:
            self.browser.quit()

    def search_maps(self, city: str, state_code: str, subject: str):
        """
        Search maps for 'subject' in 'city', 'state_code'.
        Save results to table.

        Args:
            city: str
                to search in
            state_code: str
                to search in
            subject: str
                to search for
        """
        businesses = []

        if len(state_code) != 2:
            raise custom_errors.StateCodeFormattingError(state_code=state_code,
                                                         message='State code must be two uppercase characters.')
        elif not state_code.isupper():
            state_code = state_code.upper()
        self.browser.get("https://www.google.com/maps")

        try:  # TO SEARCH SUBJECT IN CITY, STATE
            search_box = self.browser.find_element_by_css_selector(self.css_selectors['SEARCH BOX'])
            search_button = self.browser.find_element_by_css_selector(self.css_selectors['SEARCH BUTTON'])
            # SEARCH CITY TO ORIENT MAP
            search_box.send_keys(city + ', ' + state_code)
            search_button.click()
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            self.browser.save_screenshot(
                path_errors + f"{city}, {state_code} search_maps search_box_button failure.png")
            print(e, "** SEARCH BOX / BUTTON failed, resetting map **")
            self.browser.get("https://www.google.com/maps")
            sleep(8)
        else:
            try:  # TO WAIT TILL PAGE IS FULLY LOADED
                WebDriverWait(driver=self.browser, timeout=15) \
                    .until(expected_conditions
                           .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors['WIDGET & MAP'])))
                WebDriverWait(driver=self.browser, timeout=15) \
                    .until(expected_conditions
                           .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors['CLEAR SEARCH'])))
            except TimeoutException as e:
                self.browser.save_screenshot(path_errors + f"{city}, {state_code} search_maps city WIDGET & MAP "
                                                           f"CLEAR_SEARCH timeout.png")
                print(e, "** WIDGET & MAP / CLEAR SEARCH timeout, resetting map **")
                self.browser.get("https://www.google.com/maps")
                sleep(8)
            else:  # CLEAR SEARCH BOX (APPEARS AFTER SEARCH BUTTON HAS BEEN PRESSED) & SEARCH SUBJECT
                self.browser.find_element_by_css_selector(self.css_selectors['CLEAR SEARCH']).click()
                search_box.send_keys(subject + ' near ' + city + ' ' + state_code)
                search_button.click()
                try:  # TO WAIT FOR MAP TO FULLY LOAD
                    WebDriverWait(driver=self.browser, timeout=15) \
                        .until(expected_conditions
                               .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors['WIDGET & MAP'])))
                except TimeoutException as e:
                    self.browser.save_screenshot(path_errors + f"{city}, {state_code} search_maps subject WIDGET & MAP "
                                                               f"timeout.png")
                    print(e, "** WIDGET & MAP timeout, resetting map **")
                    self.browser.get("https://www.google.com/maps")
                    sleep(8)
                else:
                    try:  # TO WAIT FOR RESULTS TO FULLY LOAD
                        WebDriverWait(driver=self.browser, timeout=15) \
                            .until(expected_conditions
                                   .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors['RESULTS'])))
                    except TimeoutException:
                        self.browser.save_screenshot(
                            path_errors + f"{city}, {state_code} search_maps RESULTS timeout.png")
                        print(f'** RESULTS timeout for {city}, {state_code} **')
                    else:
                        while 1:  # RESET results VARIABLE BC OF ELEMENT STALENESS
                            results = self.browser.find_elements_by_css_selector(self.css_selectors['RESULTS'])
                            if results:
                                self.page_count += 1
                                businesses += self.iterate_businesses(city=city,
                                                                      state_code=state_code,
                                                                      businesses=results)
                                if self.page_count >= 25:
                                    sleep(60 * 60 * 4)  # SLEEP FOR 4 HRS AFTER COLLECTING 25 PAGES OF RESULTS
                                    self.page_count = 0
                            else:
                                break
                            try:
                                next_button = self.browser.find_element_by_css_selector(
                                    self.css_selectors['NEXT RESULTS PAGE'])
                            except (NoSuchElementException, ElementClickInterceptedException,
                                    ElementNotInteractableException):
                                break
                            else:
                                try:  # TO GO TO NEXT RESULTS PAGE IF IT EXISTS
                                    next_button.click()
                                    sleep(10)
                                except (NoSuchElementException, ElementClickInterceptedException,
                                        ElementNotInteractableException):
                                    break
        return businesses

    def iterate_businesses(self, city: str, state_code: str, businesses: [webelement, ...]):
        """
        iterate business entries and aggregate info

        Args:
            city: str
            state_code: str
            businesses: [ webelement, ... ]
                google maps search results
        Returns: [(name, phone, url, city, state code), ...]
            business info list
        """
        results = []
        if not businesses:
            return results

        for i in range(len(businesses)):
            biz = businesses.pop(i)
            if not biz.is_displayed() and i < 6:
                biz.location_once_scrolled_into_view

            # IF AD THEN SKIP
            try:
                ad = biz.find_element_by_css_selector(self.css_selectors['AD'])
                if ad.is_displayed() and ad.is_enabled():
                    continue
                else:
                    raise NoSuchElementException()
            except NoSuchElementException:
                try:  # TO PROCESS BUSINESS SINCE IT WASN'T AN AD
                    biz.click()
                    sleep(2)
                except (ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException):
                    self.browser.save_screenshot(path_errors + f"{city}, {state_code} iterate_businesses biz_click.png")
                    print('** iterate_businesses() biz.click() failed **')
                    continue
                else:
                    try:  # TO WAIT TILL BIZ PAGE IS FULLY LOADED
                        WebDriverWait(driver=self.browser, timeout=30) \
                            .until(expected_conditions
                                   .presence_of_element_located((By.CSS_SELECTOR,
                                                                 self.css_selectors['BUSINESS IMAGE'])))
                    except TimeoutException:  # HANDLE BIZ IMAGE LOADING TIMEOUT
                        self.browser.save_screenshot(
                            path_errors + f"{city}, {state_code}_iterate_businesses bizimg.png")
                        print('** BUSINESS IMAGE timed out **')
                        try:  # TO CLICK BACK BUTTON AFTER TIMEOUT ERROR
                            self.browser.find_element_by_css_selector(self.css_selectors['BACK TO RESULTS']).click()
                            sleep(3)
                        except (ElementClickInterceptedException, ElementNotInteractableException,
                                NoSuchElementException):
                            self.browser.save_screenshot(path_errors + f"{city}, {state_code} iterate_businesses "
                                                                       f"back_button_click after biz img timeout.png")
                            print('** BACK TO RESULTS failed after BIZ IMAGE timeout **')
                            break

                    # COLLECT BIZ INFO & ADD TO RESULTS
                    name, phone, url = self.business_info()
                    if name:
                        results.append((name, url, phone, city, state_code))

                    try:  # TO GO BACK TO RESULTS
                        element = self.browser.find_element_by_css_selector(self.css_selectors['BACK TO RESULTS'])
                        actions = ActionChains(self.browser)
                        actions.move_to_element(element)
                        actions.click(element)
                        actions.perform()
                        sleep(3)
                    except (NoSuchElementException, ElementNotInteractableException,
                            ElementClickInterceptedException) as e:
                        self.browser.save_screenshot(path_errors + f"{city}, {state_code} iterate_businesses "
                                                                   f"back_button_click.png")
                        print(e, '** BACK TO RESULTS failed after gathering biz info **')
                        break
                    else:
                        try:  # TO RELOAD RESULTS LIST BC OF STALENESS
                            WebDriverWait(driver=self.browser, timeout=30) \
                                .until(expected_conditions
                                       .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors['RESULTS'])))
                            businesses = self.browser.find_elements_by_css_selector(self.css_selectors['RESULTS'])
                        except TimeoutException:
                            self.browser.save_screenshot(path_errors + f"{city}, {state_code} iterate_businesses "
                                                                       f"RELOAD RESULTS timeout.png")
                            print('** RESULTS REFRESH timed-out **')
                            break

        print(f'-> Found {len(results)} contacts')
        return results

    def business_info(self):
        """
        Gather relevant business info from maps page

        :Returns:
            basic contact info
        """
        try:
            name = ''
            name_list = self.browser.find_element_by_css_selector(
                self.css_selectors['NAME']).get_property('innerText').split('-')
            if len(name_list) >= 2:
                name_list.pop(-1)
            for i in name_list:
                if not name:
                    name = i.strip()
                else:
                    name = name + ' - ' + i.strip()
                    name.encode('utf8')
            contact_info = self.browser.find_elements_by_css_selector("span.widget-pane-link")
        except NoSuchElementException:
            print("** business_info() FAILED **")
            return None, None, None
        else:
            # FIND PHONE NUMBER & URL IF EXISTS
            phone = None
            url = None
            for e in contact_info:
                attr = e.get_property('innerText')
                if not url and '.com' in attr:
                    url = attr.strip()
                    url.encode('utf8')
                if not phone:
                    phone = re.search(r"^\(\d\d\d\) \d\d\d-\d\d\d\d", attr)
                    if phone:
                        phone = phone[0].strip()
                        phone.encode('utf8')

            return name, url, phone
