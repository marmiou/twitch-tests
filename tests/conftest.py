import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def chrome_browser():
    # Your existing setup
    driver = webdriver.Chrome()  # Consider using ChromeDriverManager as well for dynamic binary management
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture()
def mobile_browser(request):
    device_name = request.param
    mobile_emulation = {"deviceName": device_name}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

