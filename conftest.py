import pytest
import allure
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config import MAIN_PAGE_URL, REGISTER_URL, DELETE_USER_URL
from utils.helpers import generate_user_data, register_user, delete_user
from pages.main_page import MainPage
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome или firefox",
    )


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    """
    Параметризованная фикстура драйвера.
    Запускает тесты в Chrome и Firefox.
    """
    browser = request.param

    with allure.step(f"Запуск браузера: {browser}"):
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            drv = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            drv = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
        else:
            raise ValueError(f"Неизвестный браузер: {browser}")

    drv.implicitly_wait(3)
    yield drv

    with allure.step("Закрытие браузера"):
        drv.quit()


@pytest.fixture(scope="function")
def new_user():
    """Создаёт пользователя через API и удаляет его после теста."""
    user_data = generate_user_data()
    response_body = register_user(user_data)
    access_token = response_body.get("accessToken")

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "accessToken": access_token,
    }

    delete_user(access_token)


@pytest.fixture(scope="function")
def logged_in_driver(driver, new_user):
    """
    Открывает браузер, логинит пользователя через UI и возвращает драйвер.
    """
    login_page = LoginPage(driver)
    main_page = MainPage(driver)

    with allure.step("Переходим на страницу логина"):
        login_page.open_login_page()

    with allure.step(f"Входим как {new_user['email']}"):
        login_page.login(new_user["email"], new_user["password"])

    with allure.step("Ждём загрузки главной страницы после логина"):
        main_page.find_visible(main_page.CONSTRUCTOR_HEADER)

    return driver
