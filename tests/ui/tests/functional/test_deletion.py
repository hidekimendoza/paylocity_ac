import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.benefits import BenefitsPage
from pages.login import LoginPage


class TestDeletion:

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

    @pytest.fixture(scope="function")
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
        benefits_p = BenefitsPage(driver)
        benefits_p.add_employee("first", "last", "0", verify=True)
        time.sleep(3)
        # This fixture yields the driver, keeping the session active for the test
        yield driver

    def test_single_deletion_shall_remove_one_element(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        employees_ids = benefits_p.get_column_texts(0)[1:]
        to_remove_id = employees_ids[-1]
        benefits_p.delete_employee(to_remove_id, verify=True)
        updated_employees_ids = benefits_p.get_column_texts(0)[1:]
        assert to_remove_id not in updated_employees_ids

    def test_cancel_deletion_shall_keep_all_elements(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        employees_ids = benefits_p.get_column_texts(0)[1:]
        to_remove_id = employees_ids[-1]
        employee_row = benefits_p.get_existing_employee_from_table(
            to_remove_id)
        benefits_p.click_delete_button(employee_row)
        benefits_p.cancel_deletion()
        time.sleep(5)
        updated_employees_ids = benefits_p.get_column_texts(0)[1:]
        assert len(employees_ids) == len(updated_employees_ids)
        assert set(employees_ids) == set(updated_employees_ids)

    def test_creation_header_content_shall_be_properly_set(self, logged_in_session):
        driver = logged_in_session
        benefits_p = BenefitsPage(driver)
        employees_ids = benefits_p.get_column_texts(0)[1:]
        to_remove_id = employees_ids[-1]
        employee_row = benefits_p.get_existing_employee_from_table(
            to_remove_id)
        benefits_p.click_delete_button(employee_row)
        assert "Delete Employee" == benefits_p.get_delete_title_form()
