import allure
import pytest

from pageObjects.Streamer import StreamerPage
from pageObjects.Twitch import MainPage


@allure.epic("Twitch")
@allure.story("Streamers")
@allure.title("Test Streamer has loaded with all its basic components")
@allure.severity(allure.severity_level.CRITICAL)
@allure.parent_suite("Twitch Tests suite")
@allure.suite("Streamer Tests suite")
@pytest.mark.streamer
@pytest.mark.regression
@pytest.mark.parametrize("mobile_browser", ["iPhone X", "Galaxy S5"], indirect=True)
def test_streamer_loaded(mobile_browser):
    twitch_page = MainPage(mobile_browser)
    twitch_page.go_to_url("https://m.twitch.tv/")
    twitch_page.close_cookie_modal()
    twitch_page.go_to_search()
    twitch_page.search_for("StarCraft II")
    twitch_page.scroll_down(2)
    twitch_page.click_random_streamer()

    streamer_page = StreamerPage(mobile_browser)
    elements = streamer_page.load_streamer_elements()
    streamer_page.take_screenshot()

    for element in elements:
        assert element is not None, f"Element {element} is not present in the streamer"
