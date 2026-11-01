import logging

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def chrome_browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture()
def mobile_browser(request):
    device_name = request.param

    device_metrics = {
        "iPhone X": {
            "width": 375,
            "height": 812,
            "pixelRatio": 3,
        },
        "Galaxy S5": {
            "width": 360,
            "height": 640,
            "pixelRatio": 3,
        },
    }

    mobile_emulation = {
        "deviceMetrics": device_metrics[device_name],
        "userAgent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Mobile Safari/537.36"
        ),
    }

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "mobileEmulation", mobile_emulation
    )
    chrome_options.add_argument("--start-fullscreen")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def pytest_configure(config):
    logging.basicConfig(level=logging.INFO)