from selenium.webdriver.common.by import By

from config import LOGIN_PAGE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации."""

    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Войти']")
    PAGE_HEADER = (By.XPATH, "//h2[text()='Вход']")

    def open_login_page(self):
        self.open(LOGIN_PAGE_URL)
        self.find_visible(self.PAGE_HEADER)

    def login(self, email: str, password: str):
        self.find_visible(self.EMAIL_INPUT).send_keys(email)
        self.find_visible(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.SUBMIT_BUTTON)
