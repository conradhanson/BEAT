import json
import logging
import re
from time import sleep

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# MODULE
import browser
from definitions import path_css_selectors
from definitions import path_save_errors
from definitions import default_timeout
from definitions import max_timeout


class Crawler:
    def __init__(self, width=2560, height=1600):
        """ Crawl Google Maps for business info """
        with open(path_css_selectors, 'r') as f:
            self.css_selectors = json.load(f)

        self.browser = browser.get_firefox(width=width, height=height)
        # self.browser = browser.get_chrome(width=width, height=height)
        self.page_count = 0  # keep track of number pages that have been processed

    def quit(self):
        if self.browser:
            self.browser.quit()

    def wait_for(self, key: str):
        """
        Wait for the element to fully load.

        Args:
            key: str
                CSS Selector key to wait for

        Returns: boolean
            if element fully loaded
        """
        try:
            WebDriverWait(driver=self.browser, timeout=default_timeout) \
                .until(expected_conditions
                       .presence_of_element_located((By.CSS_SELECTOR, self.css_selectors[key])))
        except TimeoutException:
            self.browser.save_screenshot(path_save_errors + f"{key} wait_for error.png")
            logging.error(f"failed to wait for {key}", exc_info=False)
            return False
        return True

    def can_click(self, key: str):
        """
        Wait until an element can be clicked.

        Args:
            key: str
                CSS Selector key of element to click

        Returns: boolean
            if element can be clicked
        """
        try:
            WebDriverWait(driver=self.browser, timeout=default_timeout) \
                .until(expected_conditions.
                       element_to_be_clickable((By.CSS_SELECTOR, self.css_selectors[key])))
        except TimeoutException:
            logging.info(f"Can't click: {key}", exc_info=False)
            return False
        return True

    def next_page(self, key: str):
        """
        go to next page of results.

        Args:
            key: str
                CSS Selector key of next element

        Returns: bool
            if next page was clicked
        """
        try:  # TO GO TO NEXT RESULTS PAGE IF IT EXISTS
            next_page_button = self.browser.find_element_by_css_selector(self.css_selectors[key])
        except NoSuchElementException:
            return False

        if next_page_button.is_enabled() and next_page_button.is_displayed():
            try:
                next_page_button.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                logging.error(f'next_page failed after button was found, enabled, and displayed.')
                return False
        else:
            return False

        return True

    def go_back_to_results(self, count: int):
        """
        Go back to the results page, try to click element for count times.
        If the button doesn't exist, then assume current state is on results page.

        Args:
            count: int
                number of times to try to click element

        Returns: boolean
        """
        key = 'BACK TO RESULTS'
        current_url = self.browser.current_url

        # FIND THE ELEMENT
        try:
            element = self.browser.find_element_by_css_selector(self.css_selectors[key])
        except NoSuchElementException:
            logging.error("Couldn't find button when trying to go back to results")
            return True

        # ATTEMPT TO CLICK ELEMENT COUNT TIMES, COMPARING BEFORE AND AFTER URLs TO DETERMINE IF SUCCESSFUL
        for i in range(0, count):
            clickable = self.can_click(key)
            if clickable:
                try:
                    element.click()
                except (ElementClickInterceptedException, ElementNotInteractableException):
                    pass

                sleep(5)
                if current_url != self.browser.current_url:
                    return True
        return False

    def is_ad(self, listing: webelement):
        """
        Check if listing is an ad

        Args:
            listing: webelement
                that you want to check

        Returns: boolean
        """
        try:
            ad = listing.find_element_by_css_selector(self.css_selectors['AD'])
        except NoSuchElementException:
            return False

        if ad.is_displayed() and ad.is_enabled():
            return True
        else:
            return False

    def get_name(self):
        """ grab a business's name """
        name = None
        try:
            name_list = self.browser.find_element_by_css_selector(self.css_selectors['NAME'])\
                .get_property('innerText').split('-')
        except NoSuchElementException:
            # logging.error("get_name failed to find element", exc_info=False)
            pass
        else:
            if len(name_list) >= 2:
                name_list.pop(-1)
            for i in name_list:
                if not name:
                    name = i.strip()
                else:
                    name = name + ' - ' + i.strip()
                    # name.encode('utf8')

        return name

    def get_url(self):
        """ grab a business's URL if it exists """
        url = None
        try:
            url = self.browser.find_element_by_css_selector(self.css_selectors["NEW URL"]).get_property('innerText')
        except NoSuchElementException:
            # logging.error("get_url failed to find element", exc_info=False)
            pass
        else:
            url = url.strip()
        return url

    def get_phone(self):
        """ grab a business's phone number if it exists """
        phone = None
        try:
            phone = self.browser.find_element_by_css_selector(self.css_selectors["NEW PHONE #"])\
                .get_property('innerText')
        except NoSuchElementException:
            # logging.error("get_phone failed to find element", exc_info=False)
            pass
        else:
            phone = re.search(r"^\(\d\d\d\) \d\d\d-\d\d\d\d", phone)
            if phone:
                phone = phone[0].strip()
        return phone

    def orient_map(self, location: str):
        """
        orient the map to the location ('city, state' or 'subject near city, state')

        Args:
            location: str
                to orient map

        Returns: boolean
            if successful
        """
        try:  # TO FIND SEARCH BOX & BUTTON
            search_box = self.browser.find_element_by_css_selector(self.css_selectors['SEARCH BOX'])
            search_button = self.browser.find_element_by_css_selector(self.css_selectors['SEARCH BUTTON'])
        except NoSuchElementException:
            self.browser.save_screenshot(path_save_errors + f"orient_map no such element error.png")
            logging.error("Failed to find search box/button", exc_info=False)
            return False

        try:  # TO SEARCH CITY TO ORIENT MAP
            search_box.send_keys(location)
            search_button.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            self.browser.save_screenshot(path_save_errors + f"orient_map click error.png")
            logging.error("Failed to click search button", exc_info=False)
            return False
        return True

    def iterate_businesses(self, city, state_code, businesses):
        """
        Find the name, URL, phone number, city, state of each business in the businesses list.

        Args:
            city: str
                that businesses are in
            state_code: str
                that businesses are in
            businesses: [WebElement, ...]

        Returns: a list of tuples for each business processed.
            (name, URL, phone number, city, state)
        """
        biz_data = []

        for i in range(len(businesses)):
            try:
                biz = businesses.pop(i)
            except IndexError:
                # logging.error(f'Failed to pop the {i}-th index of business list')
                break

            if not biz.is_displayed():
                biz.location_once_scrolled_into_view

            if self.is_ad(biz):
                continue

            # TODO this waiting for biz to be enabled doesn't work. biz is enabled but not clickable. check for clickable state instead.
            biz_enabled = biz.is_enabled()
            retry_count = 0
            while not biz_enabled:
                retry_count += 1
                if retry_count > 3:
                    break
                logging.info(f'{retry_count}-th time waiting for biz to be enabled.')
                biz_enabled = biz.is_enabled()

            if not biz_enabled:
                continue

            try:  # TO CLICK THE BUSINESS LISTING
                biz.click()
            except (ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException):
                self.browser.save_screenshot(path_save_errors + f"iterate_businesses biz_click.png")
                logging.error('iterate_businesses -> biz.click() failed', exc_info=False)
                continue

            # VERIFY BUSINESS LISTING'S IMAGE HAS LOADED
            img_loaded = self.wait_for('BUSINESS IMAGE')
            retry_count = 0
            while not img_loaded:
                retry_count += 1
                if retry_count > 3:
                    break
                logging.info(f'{retry_count}-th time waiting for BUSINESS IMAGE to load')
                img_loaded = self.wait_for('BUSINESS IMAGE')

            if not img_loaded:
                continue

            # COLLECT BUSINESS INFO & ADD TO RELEVANT RESULTS
            name = self.get_name()
            url = self.get_url()
            # phone = self.get_name()
            logging.info(f"processing business {i}-th: name='{name}' url='{url}'")
            if name and url:
                biz_data.append((name, url, city, state_code))

            # TODO maybe wrap in function?
            # GO BACK TO THE RESULTS PAGE
            successful_go_back = self.go_back_to_results(count=10)
            retry_count = 0
            while not successful_go_back:
                retry_count += 1
                if retry_count > 3:
                    break
                logging.info(f'{retry_count}-th time trying to go back to results')
                successful_go_back = self.go_back_to_results(count=10)

            if successful_go_back:
                # WAIT FOR THE RESULTS PAGE TO LOAD
                results_loaded = self.wait_for('RESULTS')
                retry_count = 0
                while not results_loaded:
                    retry_count += 1
                    if retry_count > 3:
                        break
                    logging.info(f'{retry_count}-th time waiting for results to load')
                    results_loaded = self.wait_for('RESULTS')

                if not results_loaded:
                    logging.error('RESULTS loading timeout')
                    self.browser.save_screenshot(path_save_errors +
                                                 f"{city}, {state_code} iterate_businesses RELOAD RESULTS timeout.png")
                    break
            else:
                logging.error('Unsuccessful go back to results')
                self.browser.save_screenshot(path_save_errors +
                                             f"{city}, {state_code} iterate_businesses RELOAD RESULTS timeout.png")
                break

            # REFRESH STALE BUSINESS LIST
            businesses = self.browser.find_elements_by_css_selector(self.css_selectors['RESULTS'])
        return biz_data

    def search_subject(self, city: str, state_code: str, subject: str,
                       page_limit: int = 25, sleep_time: int = max_timeout):
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
            page_limit: int
                of results processed before sleeping. Default is 25 pages of results.
            sleep_time: int
                in seconds till continuing the results processing.

        Returns: boolean
            if successful
        """
        businesses = []
        self.browser.get("https://www.google.com/maps")
        self.orient_map(city + ' ' + state_code)
        self.wait_for('WIDGET & MAP')

        if self.can_click('CLEAR SEARCH'):
            self.browser.find_element_by_css_selector(self.css_selectors['CLEAR SEARCH']).click()
            self.orient_map(subject + ' near ' + city + ' ' + state_code)
            self.wait_for('WIDGET & MAP')
            self.wait_for('RESULTS')
            results = self.browser.find_elements_by_css_selector(self.css_selectors['RESULTS'])

            while results:
                self.page_count += 1
                # logging.info(f'{len(results)} businesses to iterate over')
                businesses += self.iterate_businesses(city=city, state_code=state_code, businesses=results)

                if self.page_count >= page_limit:
                    logging.info(f"sleeping for {max_timeout / 3600} hrs")
                    sleep(sleep_time)  # SLEEP FOR X HRS AFTER COLLECTING X PAGES OF RESULTS
                    self.page_count = 0

                if self.next_page('NEXT RESULTS PAGE'):
                    if self.wait_for('RESULTS'):
                        results = self.browser.find_elements_by_css_selector(self.css_selectors['RESULTS'])
                        sleep(3)
                    else:
                        break
                else:
                    break

        return businesses
