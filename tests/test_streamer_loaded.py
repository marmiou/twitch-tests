import pytest

from pageObjects.Streamer import StreamerPage
from pageObjects.Twitch import MainPage


@pytest.mark.parametrize("mobile_browser", ["iPhone X"], indirect=True)  #'Galaxy S5'
def test_streamer_loaded(mobile_browser):
    twitch_page = MainPage(mobile_browser)
    twitch_page.go_to_url("https://m.twitch.tv/")
    twitch_page.close_cookie_modal()
    twitch_page.go_to_search()
    twitch_page.search_for("StarCraft II")
    twitch_page.scroll_down(2)
    twitch_page.click_first_visible_streamer()

    streamer_page = StreamerPage(mobile_browser)
    elements = streamer_page.all_elements()
    streamer_page.take_screenshot()

    for element in elements:
        assert element is not None, f"Element {element} is not present in the streamer"
