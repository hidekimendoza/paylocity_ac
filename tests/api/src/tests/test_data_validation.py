import uuid

import pytest
import pytest_check as check
from src.api.api_client import APIClient
from src.api.employee import Employee


class TestDataValidation:

    @pytest.fixture(scope="function")
    def clean_env(self):
        client = APIClient()
        response = client.get_all_employees()
        employee_list = response.json()
        for employee in employee_list:
            client.delete_employee_by_id(employee["id"])

    @pytest.fixture(scope="function")
    def created_employee(self):
        client = APIClient()
        post_employee = Employee("test_username", "myfirstname", "lname")

        response = client.create_employee(post_employee)
        json_response = response.json()

        yield response.json()

        client.delete_employee_by_id(json_response["id"])

    """ GET employee"""

    def test_get_from_empty_list(self, clean_env):
        client = APIClient()
        response = client.get_all_employees()
        check.equal(200, response.status_code)
        assert ([] == response.json())

    """ GET employee/{ID} """

    def test_getbyid_empty_list(self, clean_env):
        client = APIClient()
        response = client.get_employee_by_id(uuid.uuid4().hex)
        check.equal(404, response.status_code)

    def test_getbyid_not_existing_employee_non_empty_list(self, created_employee):
        client = APIClient()
        response = client.get_employee_by_id(uuid.uuid4().hex)
        check.equal(404, response.status_code)

    def test_getbyid_invalid_ids(self, created_employee):
        client = APIClient()
        invalid_format = uuid.uuid4().hex[::-1]
        invalid_format_and_length = "123"
        long_id = uuid.uuid4().hex + uuid.uuid4().hex

        response = client.get_employee_by_id(invalid_format)
        check.equal(400, response.status_code)

        response = client.get_employee_by_id(invalid_format_and_length)
        check.equal(400, response.status_code)

        response = client.get_employee_by_id(long_id)
        check.equal(400, response.status_code)

    """ POST employee """

    def test_post_required_data_only(self, clean_env, created_employee):
        post_employee = Employee(
            "DupUserName", "DupFirst", "Duplname", id=created_employee["id"])
        client = APIClient()
        response = client.create_employee(post_employee)
        print(created_employee["id"])
        print(response.content)
        check.equal(409, response.status_code)

    def test_post_custom_salary_shall_not_change_salary(self, clean_env):
        post_employee = Employee("UserName", "First", "lname", salary=555.0)
        client = APIClient()
        response = client.create_employee(post_employee)
        json_response = response.json()
        print(json_response)
        check.equal(Employee.GROSS_PAY_PER_CHECK *
                    Employee.NUM_PAYCHECKS_PER_YEAR, json_response["salary"])

    def test_post_get_nullable_elements(self, clean_env):
        employee = Employee("UserName", "First", "lname", expiration=None)
        client = APIClient()
        response = client.create_employee(employee)
        json_response = response.json()

        nullable_fields = ["expiration", "partitionKey"]
        getter_response = client.get_employee_by_id(json_response["id"]).json()
        print(getter_response)
        assert (all(field in nullable_fields for field in getter_response.keys()))

    def test_create_with_user_defined_id(self):
        defined_id = uuid.uuid4().hex
        client = APIClient()
        employee = Employee("uname", "first", "last", id=defined_id)
        response = client.create_employee(employee)
        posted_id = response.json()
        check.equal(404, response.status_code)
        assert (posted_id.get("id", None) == defined_id)

    def test_post_expired_employee_shall_not_be_available(self):
        client = APIClient()
        expired_employee = Employee(
            "uname", "first", "last", expiration="2015-06-22T04:40:35.641Z")
        response = client.create_employee(expired_employee)
        json_response = response.json()
        check.equal(404, response.status_code)
        print(json_response)

    """ UPDATE employee """

    def test_update_unexisting_employee_non_empty_list(self, clean_env):
        post_employee = Employee("DupUserName", "DupFirst", "Duplname")
        client = APIClient()
        response = client.update_employee(post_employee)
        print(response.content)
        check.equal(404, response.status_code)

    def test_update_unexisting_employee_empty_list(self):
        not_existing_employee = Employee("DupUserName", "DupFirst", "Duplname")
        client = APIClient()
        response = client.update_employee(not_existing_employee)
        check.equal(404, response.status_code)

    def test_update_update_salary(self, created_employee):
        """ User shall not be able to update salary """
        existing_id = created_employee["id"]
        updated_emp = Employee("UpdatedUsername", "UpdatedFirstname",
                               "UpdatedLastName", salary=75000.0, id=existing_id)
        client = APIClient()
        response = client.update_employee(updated_emp)
        check.equal(404, response.status_code)
