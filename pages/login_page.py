from config import LOGIN_PAGE_URL
from pages.base_page import BasePage
from pages.locators import LoginPageLocators


class LoginPage(BasePage):
    """Страница авторизации."""

    def open_login_page(self):
        self.open(LOGIN_PAGE_URL)
        self.find_visible(LoginPageLocators.PAGE_HEADER)

    def login(self, email: str, password: str):
        self.find_visible(LoginPageLocators.EMAIL_INPUT).send_keys(email)
        self.find_visible(LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.click(LoginPageLocators.SUBMIT_BUTTON)
