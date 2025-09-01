import pytest
import pytest_check as check

from src.api.api_client import APIClient
from src.api.employee import Employee


class TestCrud:
    """ Test CRUD with valid inputs and validate status code and action completion"""

    @pytest.fixture(scope="function")
    def created_employee(self):
        client = APIClient()
        post_employee = Employee("test_username", "myfirstname", "lname")

        response = client.create_employee(post_employee)
        json_response = response.json()

        yield response.json()

        client.delete_employee_by_id(json_response["id"])

    """ CRUD operations tests"""

    def test_post_employees_shall_return_successful_rc(self):
        client = APIClient()
        post_employee = Employee("test_username", "myfirstname", "lname")
        response = client.create_employee(post_employee)
        check.equal(200, response.status_code)
        employee_response = response.json()
        check.is_true(all(field in employee_response.items()
                      for field in post_employee.to_dict().items()))

    def test_get_employees_valid_employee(self, created_employee):
        client = APIClient()
        response = client.get_all_employees()
        check.equal(200, response.status_code)
        employees_list = response.json()
        check.is_instance(employees_list, list,
                          "Expected response to be a list")
        assert any(emp.get("id") ==
                   created_employee["id"] for emp in employees_list)

    def test_put_employees_existing_employee_id(self, created_employee):
        existing_id = created_employee["id"]
        updated_emp = Employee("UpdatedUsername", "UpdatedFirstname", "UpdatedLastName",
                               3, expiration="2015-06-22T04:40:35.641Z", salary=75000.0, id=existing_id)

        client = APIClient()
        response = client.update_employee(updated_emp)
        check.equal(200, response.status_code)
        json_response = response.json()
        check.is_true(all(field in json_response.items()
                      for field in updated_emp.to_dict().items()))

    def test_delete_employee_shall_return_successful_rc(self, created_employee):
        existing_id = created_employee["id"]
        client = APIClient()
        response = client.delete_employee_by_id(existing_id)
        check.equal(200, response.status_code)
        all_elements = client.get_all_employees()
        all_elements_response = all_elements.json()
        assert all(emp.get("id") !=
                   created_employee["id"] for emp in all_elements_response)

    def test_getbyid_existing_employee(self, created_employee):
        existing_id = created_employee["id"]
        client = APIClient()
        response = client.get_employee_by_id(existing_id)
        check.equal(200, response.status_code)
        json_response = response.json()
        check.is_true(all(field in json_response.items()
                      for field in json_response.items()))
