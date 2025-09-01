import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.benefits import BenefitsPage
from pages.login import LoginPage


class TestNonFunctional:

    @pytest.fixture
    def setup_and_teardown(self):
        """
        Pytest fixture to set up and tear down the WebDriver.
        It returns a WebDriver instance for the test to use.
        """
        driver = None
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            yield driver
        finally:
            if driver:
                driver.quit()

    @pytest.fixture
    def logged_in_session(self, setup_and_teardown):
        """
        Pytest fixture to perform login and save cookies for later use.
        It depends on the setup_and_teardown fixture.
        """
        driver = setup_and_teardown
        login_page = LoginPage(driver)

        login_page.login("TestUser788", "L?}'5miB/n]9")
        login_page.save_cookies()
        time.sleep(3)  # Wait for page to fully load

        # This fixture yields the driver, keeping the session active for the test
        yield driver

    def test_page_load_shall_not_throw_errors(self, logged_in_session):
        driver = logged_in_session
        browser_logs = driver.get_log("browser")
        failure_logs = [
            log for log in browser_logs if log['level'] == 'SEVERE']
        assert not failure_logs
