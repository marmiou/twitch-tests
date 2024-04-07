from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainPage:
    COOKIE_MODAL_CLASS = 'ReactModal__Body--open'
    CLOSE_BUTTON_CLASS = 'Layout-sc-1xcs6mc-0.jmTjSc'
    SEARCH_ICON_SELECTOR = 'a[aria-label="Search"]'
    SEARCH_INPUT_SELECTOR = 'input[type="search"]'
    FIRST_STREAMER_SELECTOR = '[title="ESL_CS2"]'

    def __init__(self, browser):
        self.browser = browser

    def go_to_url(self, url):
        self.browser.get(url)
        WebDriverWait(self.browser, 10).until(EC.url_matches(url))

    # TODO: Fix issue with close btn
    def close_cookie_modal(self):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, self.COOKIE_MODAL_CLASS)))
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, self.CLOSE_BUTTON_CLASS))).click()
        except:
            print("Close button of Cookie consent modal could not be clicked.")

    def search_icon(self):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_ICON_SELECTOR)))

    def search_input(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.SEARCH_INPUT_SELECTOR)))

    def go_to_search(self):
        element = self.search_icon()
        element.click()
        self.search_input()

    def search_for(self, text):
        search_input = self.search_input()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)

    def scroll_down(self, times=1):
        for _ in range(times):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.browser, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'main')))

    def find_all_streamers(self):
        return WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@class, "tw-image")]')))

    def click_first_visible_streamer(self):
        streamer_elements = self.find_all_streamers()
        first_visible_streamer = None
        for streamer_element in streamer_elements:
            if streamer_element.is_displayed():
                first_visible_streamer = streamer_element
                break
        first_visible_streamer.click()


