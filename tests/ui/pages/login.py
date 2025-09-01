import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class LoginPage:
    """
    A Page Object for managing login-related actions and cookies.
    """

    # Define a default URL and file path for cookies.
    # The user can override these during initialization.
    _DEFAULT_URL = "https://wmxrwq14uc.execute-api.us-east-1.amazonaws.com/Prod/Account/Login"
    _DEFAULT_COOKIE_FILE = "cookies.json"

    # Define locators for the login page elements.
    # It's a good practice to use By.ID as it's a stable and fast locator.
    USERNAME_INPUT = (By.ID, "Username")
    PASSWORD_INPUT = (By.ID, "Password")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Log In')]")

    def __init__(self, driver: WebDriver, url: str = _DEFAULT_URL, cookie_file: str = _DEFAULT_COOKIE_FILE):
        """
        Initializes the LoginPage object.
        """
        self.driver = driver
        self.url = url
        self.cookie_file = cookie_file

    def login(self, username, password):
        """
        Performs the login action by entering credentials and submitting the form.
        """
        self.driver.get(self.url)

        # Use explicit wait to ensure the elements are present before interacting
        wait = WebDriverWait(self.driver, 10)

        try:
            username_field = wait.until(
                ec.presence_of_element_located(self.USERNAME_INPUT))
            password_field = wait.until(
                ec.presence_of_element_located(self.PASSWORD_INPUT))
            submit_button = wait.until(
                ec.element_to_be_clickable(self.SUBMIT_BUTTON))

            username_field.send_keys(username)
            password_field.send_keys(password)
            submit_button.click()

            # Optional: Add a wait for the URL to change to confirm successful login
            wait.until(ec.url_changes(self.url))

            print("Login successful.")

        except Exception as e:
            print(f"An error occurred during login: {e}")
            raise

    def save_cookies(self):
        """
        Captures all cookies from the current session and saves them to a file.
        """
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookie_file, 'w') as f:
                json.dump(cookies, f, indent=4)
            print(f"Cookies saved to {self.cookie_file}")

        except Exception as e:
            print(f"Failed to save cookies: {e}")

    def load_cookies(self):
        """
        Loads cookies from a file and adds them to the current session.
        Note: You must navigate to a page on the same domain before adding cookies.
        """
        if not os.path.exists(self.cookie_file):
            print(f"Cookie file not found at {self.cookie_file}.")
            return

        try:
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)

            # Before adding cookies, you must be on a page of the correct domain
            self.driver.get(self.url)

            for cookie in cookies:
                # Some cookies have a 'sameSite' key that Selenium's `add_cookie` doesn't support
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                self.driver.add_cookie(cookie)

            # Refresh the page to apply the cookies and authenticate the session
            self.driver.refresh()
            print("Cookies loaded and page refreshed.")

        except Exception as e:
            print(f"Failed to load cookies: {e}")
