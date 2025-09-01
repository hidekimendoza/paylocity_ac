import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class BenefitsPage:
    """
    Page Object Model for the Benefits Dashboard page.
    """

    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[@id='add']")
    MODAL = (By.XPATH, "//h5[normalize-space()='Add Employee']")
    MODAL_DELETE_TITLE = (By.CSS_SELECTOR, "div[id='deleteModal'] h5[class='modal-title']")
    DEL_MODAL = (By.XPATH, "//div[@id='deleteModal']//div[@class='modal-body']")
    DEL_CONFIRMATION_BUTTON = (By.XPATH, "//button[@id='deleteEmployee']")
    DEL_CANCEL_BUTTON = (By.XPATH, "//div[@id='deleteModal']//button[@type='button'][normalize-space()='Cancel']")
    EMPLOYEE_FORM = (By.ID, "employee-details-form")
    DEPENDANTS_INPUT = (By.XPATH, "//input[@id='dependants']")
    FIRST_NAME_INPUT = (By.XPATH, "//input[@id='firstName']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@id='lastName']")

    SAVE_BUTTON = (By.XPATH, "//button[@id='addEmployee']")
    UPDATE_BUTTON = (By.XPATH, "//button[@id='updateEmployee']")
    MODAL_TITLE = (By.CSS_SELECTOR, "div[id='employeeModal'] h5[class='modal-title']")
    EMPLOYEE_TABLE = (By.ID, "employeesTable")
    EMPLOYEE_ROW_BY_NAME = (By.XPATH, "//table[@id='employeesTable']//tr[td[text()='{}']]")
    EDIT_ACTION_BUTTON = (By.XPATH, ".//i[contains(@class, 'fa-edit')]")
    DELETE_ACTION_BUTTON = (By.XPATH, ".//i[contains(@class, 'fa-times')]")
    BENEFIT_COST_DISPLAY = (By.ID, "total-benefit-cost")


    def __init__(self, driver: WebDriver):
        """
        Initializes the BenefitsPage with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def add_employee(self, first_name, last_name, dependants, verify=False):
        """
        Scenario 1: Adds a new employee to the benefits dashboard.

        GIVEN an Employer AND I am on the Benefits Dashboard page
        WHEN I select Add Employee THEN I should be able to enter employee details
        AND the employee should save AND I should see the employee in the table
        AND the benefit cost calculations are correct.
        """

        self.click_add_employee()
        self.fill_up_add_employee_form(dependants, first_name, last_name)
        self.save_add_form()
        if verify:
            self.verify_table_element_added(first_name)

    def verify_table_element_added(self, first_name):
        # Acceptance Criteria Validation
        # 1. The employee should save and appear in the table.
        # This part requires waiting for the row to appear. We'll use a dynamic locator.
        employee_row_locator = (By.XPATH, f".//td[contains(text(), {first_name})]")
        try:
            _ = self.wait.until(ec.presence_of_element_located(employee_row_locator))
            print(f"Successfully added employee '{first_name}'. Employee row is visible.")
        except TimeoutException:
            raise AssertionError(f"Employee '{first_name}' did not appear in the table after saving.")
        try:
            total_cost_text = self.driver.find_element(*self.BENEFIT_COST_DISPLAY).text
            print(f"Total benefit cost is: {total_cost_text}")
            # Add an assertion in the test file, e.g., assert total_cost_text == expected_cost
        except NoSuchElementException:
            print("Benefit cost display element not found. Cannot validate cost.")

    def save_add_form(self, wait_table_appears=True):
        # Click the "Save" button
        self.driver.find_element(*self.SAVE_BUTTON).click()
        if wait_table_appears:
            second_row = (By.CSS_SELECTOR, "#employeesTable > tbody > tr:nth-child(2)")
            self.wait.until(visibility_of_element_located(second_row))
        time.sleep(3) # Sleep added due to problem on loading table

    def save_update_form(self, wait_table_appears=True):
        # Click the "Save" button
        self.driver.find_element(*self.UPDATE_BUTTON).click()
        if wait_table_appears:
            second_row = (By.CSS_SELECTOR, "#employeesTable > tbody > tr:nth-child(2)")
            self.wait.until(visibility_of_element_located(second_row))
        time.sleep(3) # Sleep added due to problem on loading table

    def fill_up_add_employee_form(self, dependants, first_name, last_name):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.DEPENDANTS_INPUT).send_keys(dependants)

    def click_add_employee(self):
        # Click the "Add Employee" button
        add_btn = self.wait.until(ec.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON))
        add_btn.click()
        # Wait for the modal dialog to be visible before interacting with the form
        self.wait.until(ec.visibility_of_element_located(self.MODAL))

    def edit_employee(self, id: str, new_first: str, new_last: str, new_deps:int, validate=False):
        """
        Scenario 2: Edits an existing employee's details.

        GIVEN an Employer AND I am on the Benefits Dashboard page
        WHEN I select the Action Edit THEN I can edit employee details
        AND the data should change in the table.
        """

        employee_row = self.get_existing_employee_from_table(id)
        self.click_edit_button(employee_row)
        self.fill_up_edit_form(new_deps, new_first, new_last)
        self.save_update_form()
        if validate:
            self.validate_edit_employee(employee_row, new_first)

    def validate_edit_employee(self, employee_row, new_first):
        # Acceptance Criteria Validation
        # 1. The data should change in the table.
        # Wait for the old employee name to disappear and the new one to appear.
        try:
            self.wait.until(ec.staleness_of(employee_row))
            employee_row_locator = (By.XPATH, f".//td[contains(text(), {new_first})]")
            self.wait.until(ec.presence_of_element_located(employee_row_locator))
        except TimeoutException:
            raise AssertionError("Employee data did not change in the table after editing.")

    def fill_up_edit_form(self, new_deps, new_first, new_last):
        f_name_input = self.driver.find_element(*self.FIRST_NAME_INPUT)
        l_name_input = self.driver.find_element(*self.LAST_NAME_INPUT)
        dependants_input = self.driver.find_element(*self.DEPENDANTS_INPUT)
        f_name_input.clear()
        f_name_input.send_keys(new_first)
        l_name_input.clear()
        l_name_input.send_keys(new_last)
        dependants_input.clear()
        dependants_input.send_keys(new_deps)

    def click_edit_button(self, employee_row):
        # Click the "Edit" button for that employee's row
        edit_button = employee_row.find_element(*self.EDIT_ACTION_BUTTON)
        edit_button.click()
        # Wait for the modal to appear before interacting with the form
        self.wait.until(ec.visibility_of_element_located(self.MODAL))

    def get_existing_employee_from_table(self, id):
        # Find the row for the specified employee
        employee_row_locator = (By.XPATH, self.EMPLOYEE_ROW_BY_NAME[1].format(id))
        try:
            employee_row = self.wait.until(ec.presence_of_element_located(employee_row_locator))
        except TimeoutException:
            raise NoSuchElementException(f"Employee '{id}' not found in the table.")
        return employee_row

    def delete_employee(self, id: str, verify=False):
        """
        Scenario 3: Deletes an employee from the benefits dashboard.

        GIVEN an Employer AND I am on the Benefits Dashboard page
        WHEN I click the Action X THEN the employee should be deleted.
        """

        employee_row = self.get_existing_employee_from_table(id)
        self.click_delete_button(employee_row)
        self.confirm_deletion()

        if verify:
            self.validate_employee_deletion(employee_row, id)
        time.sleep(3)

    def confirm_deletion(self):
        self.driver.find_element(*self.DEL_CONFIRMATION_BUTTON).click()

    def cancel_deletion(self):
        self.driver.find_element(*self.DEL_CANCEL_BUTTON).click()

    def validate_employee_deletion(self, employee_row, id):
        # Acceptance Criteria Validation
        # 1. The employee should be deleted.
        # This requires waiting for the employee row to disappear from the table.
        try:
            self.wait.until(ec.staleness_of(employee_row))
            print(f"Successfully deleted employee '{id}'. Row is no longer visible.")
        except TimeoutException:
            raise AssertionError(f"Employee '{id}' was not deleted from the table.")

    def click_delete_button(self, employee_row):
        # Click the "Delete" button (X) for that employee's row
        delete_button = employee_row.find_element(*self.DELETE_ACTION_BUTTON)
        delete_button.click()

    def get_number_of_rows(self) -> int:
        """
        Gets the total number of rows in the table, including the header row.
        """
        table_element =  self.driver.find_element(*self.EMPLOYEE_TABLE)
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        return len(rows)

    def get_title_form(self):
        element = self.driver.find_element(*self.MODAL_TITLE)
        return element.text

    def get_delete_title_form(self):
        element = self.driver.find_element(*self.MODAL_DELETE_TITLE)
        return element.text

    def get_column_texts(self, column_index: int) -> list[str]:
        """
        Gets all text elements from a specific column of the table.
        """
        texts = []
        try:
            # Find all rows in the table, including the header row
            table_element = self.driver.find_element(*self.EMPLOYEE_TABLE)
            rows = self.driver.find_elements(By.XPATH, "//table[@id='employeesTable']//tr")

            for row in rows:
                cells = row.find_elements(By.XPATH, f"./*[{column_index + 1}]")
                if cells:
                    texts.append(cells[0].text)

        except Exception as e:
            print(f"An error occurred while getting column texts: {e}")

        return texts