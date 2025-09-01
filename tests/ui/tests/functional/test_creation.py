import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.benefits import BenefitsPage
from pages.login import LoginPage


class TestCreation:

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

        # Perform login and save the cookies
        print("\n[Fixture] Logging in and saving cookies...")
        login_page.login("TestUser788", "L?}'5miB/n]9")
        login_page.save_cookies()
        time.sleep(3) # Wait for page to fully load

        # This fixture yields the driver, keeping the session active for the test
        yield driver

    def test_single_creation_shall_create_one_element(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        prev_rows = benefits_p.get_number_of_rows()
        benefits_p.add_employee("first", "last", "0", verify=True)
        assert (prev_rows + 1) == benefits_p.get_number_of_rows()

    def test_duplicate_creation_shall_create_two_elements(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        prev_rows = benefits_p.get_number_of_rows()
        benefits_p.add_employee("first", "last", "0", verify=True)
        benefits_p.add_employee("first", "last", "0", verify=True)
        assert (prev_rows + 2) == benefits_p.get_number_of_rows()

    def test_creation_header_content_shall_be_properly_set(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        benefits_p.click_add_employee()
        assert "Add Employee" == benefits_p.get_title_form()

    def test_creation_empty_form_shall_not_be_set_as_request(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        benefits_p.click_add_employee()
        benefits_p.save_add_form(False)
        browser_logs = driver.get_log("browser")
        error_msg = "Failed to load resource: the server responded with a status of 405 "
        failure_logs = [log for log in browser_logs if error_msg in log['message']]
        assert not failure_logs

    @pytest.mark.parametrize("invalid_name", [
        ("!!!! 1111"),
        ("         invalid"),
    ])
    def test_creation_invalid_first_name_shall_not_create(self, logged_in_session, invalid_name):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)

        prev_rows = benefits_p.get_number_of_rows()
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(0, invalid_name, "lname")
        benefits_p.save_add_form(True)

        assert prev_rows == benefits_p.get_number_of_rows()

    @pytest.mark.parametrize("oor_ch", [
        "",
        (str('a' * 51))
    ])
    def test_creation_out_of_range_chars_first_name_shall_not_send_request(self, logged_in_session, oor_ch):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(0, oor_ch, "lname")
        benefits_p.save_add_form(False)
        browser_logs = driver.get_log("browser")
        error_msg = "Failed to load resource: the server responded with a status of 400"
        failure_logs = [log for log in browser_logs if error_msg in log['message']]
        assert not failure_logs

    @pytest.mark.parametrize("invalid_name", [
        ("!!!! 1111"),
        ("         invalid"),
    ])
    def test_creation_invalid_last_name_shall_not_create(self, logged_in_session, invalid_name):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)

        prev_rows = benefits_p.get_number_of_rows()
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(0, invalid_name, "lname")
        benefits_p.save_add_form(True)

        assert prev_rows == benefits_p.get_number_of_rows()

    @pytest.mark.parametrize("oor_ch", [
        "",
        (str('a' * 51))
    ])
    def test_creation_out_of_range_chars_last_name_shall_not_send_request(self, logged_in_session, oor_ch):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(0, "fname", oor_ch)
        benefits_p.save_add_form(False)
        browser_logs = driver.get_log("browser")
        error_msg = "Failed to load resource: the server responded with a status of 400"
        failure_logs = [log for log in browser_logs if error_msg in log['message']]
        assert not failure_logs

    @pytest.mark.parametrize("invalid_deps", [
        ("!!!! 1111"),
        ("2.3"),
        ("0xa"),
        ("1asd2"),
    ])
    def test_creation_invalid_dependants_shall_not_create(self, logged_in_session, invalid_deps):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)

        prev_rows = benefits_p.get_number_of_rows()
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(invalid_deps, "fname", "lname")
        benefits_p.save_add_form(True)

        assert prev_rows == benefits_p.get_number_of_rows()

    @pytest.mark.parametrize("oor_ch", [
        -1,
        33
    ])
    def test_creation_out_of_range_chars_dependants_shall_not_send_request(self, logged_in_session, oor_ch):
        driver = logged_in_session

        benefits_p = BenefitsPage(driver)
        benefits_p.click_add_employee()
        benefits_p.fill_up_add_employee_form(oor_ch, "fname", "lname")
        benefits_p.save_add_form(False)
        browser_logs = driver.get_log("browser")
        error_msg = "Failed to load resource: the server responded with a status of 400"
        failure_logs = [log for log in browser_logs if error_msg in log['message']]
        assert not failure_logs