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

    def __init__(self, browser):
        self.browser = browser

    def find_element_by_css_selector(self, css_selector):
        return WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def find_element_by_xpath(self, xpath):
        return WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

    def streamer_name(self):
        return self.find_element_by_css_selector(self.STREAMER_NAME_CSS_SELECTOR)

    def follow_button(self):
        return self.find_element_by_css_selector(self.FOLLOW_BUTTON_CSS_SELECTOR)

    def dropdown_menu(self):
        return self.find_element_by_css_selector(self.DROPDOWN_MENU_CSS_SELECTOR)

    def welcome_to_chat_room_msg(self):
        return self.find_element_by_xpath(self.WELCOME_TO_CHAT_ROOM_XPATH)

    def go_to_all_games_page_icon(self):
        return self.find_element_by_css_selector(
            self.GO_TO_ALL_GAMES_PAGE_ICON_CSS_SELECTOR
        )

    def show_top_navigation_menu_icon(self):
        return self.find_element_by_css_selector(
            self.SHOW_TOP_NAVIGATION_MENU_ICON_CSS_SELECTOR
        )

    def search_icon(self):
        return self.find_element_by_css_selector(self.SEARCH_ICON_CSS_SELECTOR)

    def send_msg_input(self):
        return self.find_element_by_xpath(self.SEND_MSG_INPUT_XPATH)

    def chat_btn(self):
        return self.find_element_by_xpath(self.CHAT_BTN_XPATH)

    def get_video(self):
        return self.find_element_by_css_selector(self.VIDEO_CSS_SELECTOR)

    def get_unavailable_video(self):
        return self.browser.find_element(
            By.XPATH,
            "//p[contains(text(), 'This video is only available for subscribers.')]",
        )

    def is_video_loaded(self):
        try:
            video_element = self.get_video()
            ready_state = self.browser.execute_script(self.READY_STATE, video_element)
            return ready_state > 0
        except Exception as e:
            return False

    def get_loaded_video(self, timeout=30, retry_interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_video_loaded():
                return self.get_video()
            else:
                unavailable_video = self.browser.find_elements(
                    By.XPATH,
                    "//p[contains(text(), 'This video is only available for subscribers.')]",
                )
                if unavailable_video:
                    return unavailable_video[0]
            time.sleep(retry_interval)
        raise TimeoutException(
            "Video did not load within the specified timeout period."
        )

    def get_loaded_chat(self):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.CHAT_MSG))
        )

    def load_streamer_elements(self):
        streamer_elements = [
            self.go_to_all_games_page_icon(),
            self.show_top_navigation_menu_icon(),
            self.search_icon(),
            self.streamer_name(),
            self.follow_button(),
            self.dropdown_menu(),
            self.welcome_to_chat_room_msg(),
            self.send_msg_input(),
            self.chat_btn(),
            self.get_loaded_video(),
            self.get_loaded_chat(),
        ]

        try:
            pop_up_window = WebDriverWait(self.browser, 15).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "//h3[contains(text(), 'Just one second...')]")
                )
            )
            if pop_up_window:
                close_button = pop_up_window.find_element(
                    By.XPATH, "//button[contains(., 'Start Watching')]"
                )
                close_button.click()
        except:
            pass

        return streamer_elements

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
