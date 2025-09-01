import requests
import uuid
import json
from src.api.employee import Employee

URL = "https://wmxrwq14uc.execute-api.us-east-1.amazonaws.com/Prod"


class APIClient:
    """
    API client for Paylocity Benefits, following the Page Object Model (POM) pattern.
    """

    def __init__(self, base_url=URL, api_key="VGVzdFVzZXI3ODg6TD99JzVtaUIvbl05"):
        self.base_url = base_url
        self.session = requests.Session()
        self.api_key = api_key

    def _get_headers(self):
        """Helper method to get standard headers, including authentication."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_key}"
        }

    def get_all_employees(self):
        """
        Gets all employees from the API.
        GET /api/Employees
        """
        url = f"{self.base_url}/api/Employees"
        response = self.session.get(url, headers=self._get_headers())
        return response

    def create_employee(self, employee, only_set_required=False):
        """
        Creates a new employee.
        POST /api/Employees
        """
        if not isinstance(employee, Employee):
            raise TypeError("Input must be an instance of the Employee class.")
        url = f"{self.base_url}/api/Employees"
        headers = self._get_headers()
        if only_set_required:
            payload = json.dumps(employee.required_fields_to_dict())
        else:
            payload = json.dumps(employee.to_dict())
        response = self.session.post(url, headers=headers, data=payload)
        return response

    def get_employee_by_id(self, employee_id):
        """
        Gets a single employee by their ID.
        GET /api/Employees/{id}
        """
        if not isinstance(employee_id, str):
            raise TypeError("Employee ID must be a string.")
        # try:
        #     uuid.UUID(employee_id, version=4)
        # except ValueError:
        #     raise ValueError("Employee ID must be a valid UUID.")
        url = f"{self.base_url}/api/Employees/{employee_id}"
        response = self.session.get(url, headers=self._get_headers())
        return response

    def update_employee(self, employee):
        """
        Updates an existing employee.
        PUT /api/Employees
        """
        if not isinstance(employee, Employee):
            raise TypeError("Input must be an instance of the Employee class.")
        url = f"{self.base_url}/api/Employees"
        headers = self._get_headers()
        payload = json.dumps(employee.to_dict())
        response = self.session.put(url, headers=headers, data=payload)
        return response

    def delete_employee_by_id(self, employee_id):
        """
        Deletes a single employee by their ID.
        DELETE /api/Employees/{id}
        """
        if not isinstance(employee_id, str):
            raise TypeError("Employee ID must be a string.")
        try:
            uuid.UUID(employee_id, version=4)
        except ValueError:
            raise ValueError("Employee ID must be a valid UUID.")
        url = f"{self.base_url}/api/Employees/{employee_id}"
        response = self.session.delete(url, headers=self._get_headers())
        return response
