import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainPage:
    COOKIE_MODAL_CLASS = "ReactModal__Body--open"
    COOKIE_POPUP_CSS_SELECTOR = ".ScTransitionBase-sc-hx4quq-0"
    CLOSE_BUTTON_XPATH = '//button[contains(., "Close")]'
    SEARCH_ICON_SELECTOR = 'a[aria-label="Search"]'
    SEARCH_INPUT_SELECTOR = 'input[type="search"]'
    FIRST_STREAMER_SELECTOR = '[title="ESL_CS2"]'
    ONLY_STREAMER_ELEMENTS_XPATH = "//section[contains(div/p, 'CHANNELS')]//img[@class='tw-image'] | //section[contains(div/p, 'People searching for \"Starcraft II\" also watch:')]//img[@class='tw-image'] | //section[contains(div/p, 'VIDEOS')]//img[@class='tw-image']"

    def __init__(self, browser):
        self.browser = browser
        logging.basicConfig(level=logging.INFO)

    def go_to_url(self, url):
        logging.info(f"Navigating to URL: {url}")
        self.browser.get(url)
        WebDriverWait(self.browser, 10).until(EC.url_matches(url))

    def close_cookie_modal(self):
        logging.info("Closing cookie modal")
        cookie_popup = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.COOKIE_POPUP_CSS_SELECTOR)
            )
        )
        close_button = cookie_popup.find_element(By.XPATH, self.CLOSE_BUTTON_XPATH)
        close_button.click()

    def search_icon(self):
        logging.info("Finding search icon")
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_ICON_SELECTOR))
        )

    def search_input(self):
        logging.info("Finding search input")
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.SEARCH_INPUT_SELECTOR)
            )
        )

    def go_to_search(self):
        logging.info("Navigating to search")
        element = self.search_icon()
        element.click()
        self.search_input()

    def search_for(self, text):
        logging.info(f"Searching for: {text}")
        search_input = self.search_input()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)

    def scroll_down(self, times=1):
        logging.info(f"Scrolling down {times} times")
        initial_scroll_position = self.browser.execute_script(
            "return window.pageYOffset;"
        )

        for _ in range(times):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

        final_scroll_position = self.browser.execute_script(
            "return window.pageYOffset;"
        )

        if final_scroll_position > initial_scroll_position:
            logging.info("Scrolling was successful.")
        else:
            logging.warning("Scrolling did not occur as expected.")

    def find_all_streamers(self):
        logging.info("Finding all streamers")
        return WebDriverWait(self.browser, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, self.ONLY_STREAMER_ELEMENTS_XPATH)
            )
        )

    def is_element_on_screen(self, element):
        logging.info("Checking if stream element is on screen")
        return element.location_once_scrolled_into_view["y"] >= 0

    def click_random_streamer(self):
        logging.info("Clicking random streamer")
        streamer_elements = self.find_all_streamers()

        visible_streamer_elements = [
            element
            for element in streamer_elements
            if element.is_displayed() and self.is_element_on_screen(element)
        ]

        if visible_streamer_elements:
            random_streamer = random.choice(visible_streamer_elements)
            self.browser.execute_script(
                "arguments[0].scrollIntoView();", random_streamer
            )
            random_streamer.click()
        else:
            logging.warning("No visible streamer found.")
