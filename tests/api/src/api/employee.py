class Employee:
    """
    A class to represent an Employee, based on the OpenAPI schema.
    """

    # Assumptions based on the provided data
    GROSS_PAY_PER_CHECK = 2000.00
    ANNUAL_EMPLOYEE_BENEFIT_COST = 1000.00
    ANNUAL_DEPENDENT_COST = 500.00
    NUM_PAYCHECKS_PER_YEAR = 26

    @classmethod
    def calculate_benefit_cost_per_check(cls, no_dependants):
        total_annual_benefit_cost = cls.ANNUAL_EMPLOYEE_BENEFIT_COST + \
            (no_dependants * cls.ANNUAL_DEPENDENT_COST)

        # Calculate the benefit cost per paycheck
        benefit_cost_per_check = total_annual_benefit_cost / cls.NUM_PAYCHECKS_PER_YEAR

        return round(benefit_cost_per_check, 2)

    @classmethod
    def calculate_net_pay_per_check(cls, no_dependants):
        total_annual_benefit_cost = cls.ANNUAL_EMPLOYEE_BENEFIT_COST + \
            (no_dependants * cls.ANNUAL_DEPENDENT_COST)

        # Calculate the benefit cost per paycheck
        benefit_cost_per_check = total_annual_benefit_cost / cls.NUM_PAYCHECKS_PER_YEAR

        # Calculate the net pay per paycheck
        net_pay_per_check = cls.GROSS_PAY_PER_CHECK - benefit_cost_per_check
        return round(net_pay_per_check, 2)

    def __init__(self, username, firstName, lastName, dependants=0, expiration=None, salary=0.0, id=None):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.dependants = dependants
        self.expiration = expiration
        self.salary = salary
        self.id = id
        # Read only fields
        # "partitionKey": "TestUser788",
        # "sortKey": "007e6bcc-443e-4716-8709-4067b8edfb1d",
        # "gross": 2000,
        # "benefitsCost": 38.46154,
        # "net": 1961.5385

    def required_fields_to_dict(self):
        return {
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName
        }

    def to_dict(self):
        """Converts the Employee object to a dictionary for JSON serialization."""
        if self.id:
            return {
                "username": self.username,
                "firstName": self.firstName,
                "lastName": self.lastName,
                "dependants": self.dependants,
                "expiration": self.expiration,
                "salary": self.salary,
                "id": self.id
            }
        return {
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "dependants": self.dependants,
            "expiration": self.expiration,
            "salary": self.salary
        }
