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
    mobile_emulation = {"deviceName": device_name}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--start-fullscreen")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def pytest_configure(config):
    logging.basicConfig(level=logging.INFO)
