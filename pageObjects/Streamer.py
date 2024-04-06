from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import shutil


class StreamerPage:
    def __init__(self, browser):
        self.browser = browser

    def take_screenshot(self):
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, '#__next div.Layout-sc-1xcs6mc-0.sc-92c0556c-1.eTHirb.eQandr  video')))
        current_directory = os.getcwd()
        screenshot_path = os.path.join(current_directory, 'streamer_page.png')
        self.browser.save_screenshot(screenshot_path)

        destination_directory = os.path.join(current_directory, 'reports', 'screenshots')
        os.makedirs(destination_directory, exist_ok=True)
        shutil.move(screenshot_path, os.path.join(destination_directory, 'streamer_page.png'))

    def video(self):
        return WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'video')))
    def streamer_name(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.CoreText-sc-1txzju1-0.kNTExs')))

    def follow_button(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-a-target="tw-core-button-label-text"]')))

    # def dropdown_menu(self):
    #     return WebDriverWait(self.browser, 10).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria_label="Open Dropdown Menu"]')))

    def welcome_to_chat_room_msg(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '//div[contains(text(), "Welcome to the chat room!")]')))

    def go_to_all_games_page_icon(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Go to all games page"]')))

    def show_top_navigation_menu_icon(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Show top navigation menu"]')))

    def search_icon(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Search"]')))

    def send_msg_input(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '//div[contains(text(), "Send a message")]')))

    def chat_btn(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '//div[contains(text(), "Chat")]')))

    def all_elements(self):
        return [
            self.go_to_all_games_page_icon(),
            self.show_top_navigation_menu_icon(),
            self.search_icon(),
            self.video(),
            self.streamer_name(),
            self.follow_button(),
            #TODO: Following selectors need fixing
            # self.dropdown_menu(),
            # self.welcome_to_chat_room_msg(),
            self.send_msg_input(),
            self.chat_btn()
            ]



