import logging
import os
import shutil
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class StreamerPage:
    VIDEO_CSS_SELECTOR = "video"
    STREAMER_NAME_CSS_SELECTOR = "p.CoreText-sc-1txzju1-0.kNTExs"
    STREAMER_NAME_SUBSCRIBED_CSS_SELECTOR = "p.CoreText-sc-1txzju1-0"
    FOLLOW_BUTTON_CSS_SELECTOR = 'div[data-a-target="tw-core-button-label-text"]'
    DROPDOWN_MENU_CSS_SELECTOR = '[aria-label="Open Dropdown Menu"]'
    WELCOME_TO_CHAT_ROOM_XPATH = '//div[contains(text(), "Welcome to the chat room!")]'
    GO_TO_ALL_GAMES_PAGE_ICON_CSS_SELECTOR = '[aria-label="Go to all games page"]'
    SHOW_TOP_NAVIGATION_MENU_ICON_CSS_SELECTOR = (
        '[aria-label="Show top navigation menu"]'
    )
    SEARCH_ICON_CSS_SELECTOR = '[aria-label="Search"]'
    SEND_MSG_INPUT_XPATH = '//p[contains(text(), "Send a message")]'
    CHAT_BTN_XPATH = '//p[contains(@class, "CoreText-sc-1txzju1-0 UFdlN") and contains(text(), "Chat")]'
    REPORTS_DIR = "reports"
    SCREENSHOT_DIR = "screenshots"
    SCREENSHOT_IMAGE = "screenshot.png"
    READY_STATE = "return arguments[0].readyState;"
    CHAT_MSG = 'div[dir="auto"]'
    UNAVAILABLE_VIDEO_XPATH = (
        '//p[contains(text(), "This video is only available for subscribers.")]'
    )
    MUTED_VIDEO_XPATH = (
        "//p[contains(text(), 'Audio for portions of this video has been muted as it appears to contain copyrighted content owned or controlled by a third party.'",
    )
    PREVENTIVE_HEADER_XPATH = "//h3[contains(text(), 'Just one second...')]"
    START_WATCHING_BTN_XPATH = "//button[contains(., 'Start Watching')]"

    def __init__(self, browser):
        self.browser = browser
        logging.basicConfig(level=logging.INFO)

    def find_element_by_css_selector(self, css_selector):
        logging.info(f"Finding element by CSS selector: {css_selector}")
        return WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def find_element_by_xpath(self, xpath):
        logging.info(f"Finding element by XPath: {xpath}")
        return WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

    def streamer_name(self):
        logging.info("Finding streamer name")
        return self.find_element_by_css_selector(self.STREAMER_NAME_CSS_SELECTOR)

    def streamer_name_subscribed(self):
        logging.info("Finding streamer name for videos available only in subscriptions")
        return self.find_element_by_css_selector(
            self.STREAMER_NAME_SUBSCRIBED_CSS_SELECTOR
        )

    def follow_button(self):
        logging.info("Finding follow button")
        return self.find_element_by_css_selector(self.FOLLOW_BUTTON_CSS_SELECTOR)

    def dropdown_menu(self):
        logging.info("Finding dropdown menu")
        return self.find_element_by_css_selector(self.DROPDOWN_MENU_CSS_SELECTOR)

    def welcome_to_chat_room_msg(self):
        logging.info("Finding welcome message in chat room")
        return self.find_element_by_xpath(self.WELCOME_TO_CHAT_ROOM_XPATH)

    def go_to_all_games_page_icon(self):
        logging.info("Finding 'Go to all games page' icon")
        return self.find_element_by_css_selector(
            self.GO_TO_ALL_GAMES_PAGE_ICON_CSS_SELECTOR
        )

    def show_top_navigation_menu_icon(self):
        logging.info("Finding 'Show top navigation menu' icon")
        return self.find_element_by_css_selector(
            self.SHOW_TOP_NAVIGATION_MENU_ICON_CSS_SELECTOR
        )

    def search_icon(self):
        logging.info("Finding search icon")
        return self.find_element_by_css_selector(self.SEARCH_ICON_CSS_SELECTOR)

    def send_msg_input(self):
        logging.info("Finding message input field")
        return self.find_element_by_xpath(self.SEND_MSG_INPUT_XPATH)

    def chat_btn(self):
        logging.info("Finding chat button")
        return self.find_element_by_xpath(self.CHAT_BTN_XPATH)

    def get_video(self):
        logging.info("Finding video element")
        return self.find_element_by_css_selector(self.VIDEO_CSS_SELECTOR)

    def get_unavailable_video_locator(self):
        logging.info("Finding unavailable video element")
        return self.find_element_by_xpath(self.UNAVAILABLE_VIDEO_XPATH)

    def get_muted_video_locator(self):
        logging.info("Finding muted video element")
        return self.browser.find_element_by_xpath(self.MUTED_VIDEO_XPATH)

    def handle_pop_up(self):
        logging.info("Checking for preventive pop up in the streamer")
        pop_up_window = None
        try:
            pop_up_window = self.find_element_by_xpath(self.PREVENTIVE_HEADER_XPATH)
            if pop_up_window:
                pop_up_window.find_element(
                    By.XPATH, self.START_WATCHING_BTN_XPATH
                ).click()
        except Exception:
            logging.info("No preventive pop up window appeared on the screen")

    def is_video_unavailable(self):
        logging.info("Checking if video is unavailable without subscription")
        try:
            unavailable_video = self.get_unavailable_video_locator()
            return True if unavailable_video else False
        except:
            logging.info("Video appears to be available")
            return False

    def get_unavailable_video(self):
        return [
            self.go_to_all_games_page_icon(),
            self.show_top_navigation_menu_icon(),
            self.search_icon(),
            self.streamer_name_subscribed(),
            self.dropdown_menu(),
            self.get_unavailable_video_locator(),
        ]

    def is_video_muted(self):
        logging.info("Checking if video is muted")
        try:
            muted_video = self.get_muted_video_locator()
            return True if muted_video else False
        except:
            logging.info("Video appears to be muted")
            return False

    def get_muted_video(self):
        return [
            self.go_to_all_games_page_icon(),
            self.show_top_navigation_menu_icon(),
            self.search_icon(),
            self.streamer_name_subscribed(),
            self.dropdown_menu(),
            self.get_muted_video_locator(),
        ]

    def is_video_loaded(self):
        logging.info("Checking if video is available")
        try:
            video_element = self.get_video()
            ready_state = self.browser.execute_script(self.READY_STATE, video_element)
            return ready_state > 0
        except Exception as e:
            logging.error(f"Error checking video load status: {e}")
            return False

    def get_loaded_video(self):

        return [
            self.go_to_all_games_page_icon(),
            self.show_top_navigation_menu_icon(),
            self.search_icon(),
            self.streamer_name(),
            self.follow_button(),
            self.dropdown_menu(),
            self.welcome_to_chat_room_msg(),
            self.send_msg_input(),
            self.chat_btn(),
            self.get_video(),
            self.get_loaded_chat(),
        ]

    def get_loaded_chat(self):
        logging.info("Waiting for chat to load")
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.CHAT_MSG))
        )

    def load_streamer_elements(self):

        self.handle_pop_up()
        if self.is_video_unavailable():
            return self.get_unavailable_video()
        elif self.is_video_muted():
            return self.get_muted_video()
        elif self.is_video_loaded():
            return self.get_loaded_video()

    def take_screenshot(self):
        current_directory = os.getcwd()
        screenshot_path = os.path.join(current_directory, self.SCREENSHOT_IMAGE)
        self.browser.save_screenshot(screenshot_path)

        destination_directory = os.path.join(
            current_directory, self.REPORTS_DIR, self.SCREENSHOT_DIR
        )
        os.makedirs(destination_directory, exist_ok=True)
        shutil.move(
            screenshot_path, os.path.join(destination_directory, self.SCREENSHOT_IMAGE)
        )
        logging.info("Screenshot taken and saved successfully")
