import allure
import pytest

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from config import MAIN_PAGE_URL, ORDER_FEED_URL


@allure.epic("Stellar Burgers UI")
@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.story("Навигация")
    @allure.title("[{driver}] Переход по клику на «Конструктор»")
    def test_click_constructor_nav_opens_constructor(self, driver):
        order_feed_page = OrderFeedPage(driver)
        main_page = MainPage(driver)

        with allure.step("Открываем страницу ленты заказов"):
            order_feed_page.open_order_feed()

        with allure.step("Кликаем на пункт меню «Конструктор»"):
            main_page.click_constructor_nav()

        with allure.step("Проверяем, что открылся конструктор бургеров"):
            assert main_page.is_constructor_visible(), \
                "Заголовок 'Соберите бургер' не отображается после перехода в Конструктор"

    @allure.story("Навигация")
    @allure.title("[{driver}] Переход по клику на «Лента заказов»")
    def test_click_order_feed_nav_opens_order_feed(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Кликаем на пункт меню «Лента заказов»"):
            main_page.click_order_feed_nav()

        with allure.step("Проверяем, что открылась лента заказов"):
            assert order_feed_page.is_order_feed_visible(), \
                "Заголовок 'Лента заказов' не отображается после перехода"

    @allure.story("Модальное окно ингредиента")
    @allure.title("[{driver}] Клик по ингредиенту открывает модальное окно с деталями")
    def test_click_ingredient_opens_modal(self, driver):
        main_page = MainPage(driver)

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Кликаем на первый ингредиент"):
            main_page.click_first_ingredient()

        with allure.step("Проверяем, что модальное окно с деталями ингредиента открылось"):
            assert main_page.is_ingredient_modal_open(), \
                "Модальное окно 'Детали ингредиента' не появилось после клика по ингредиенту"

    @allure.story("Модальное окно ингредиента")
    @allure.title("[{driver}] Модальное окно закрывается кликом по крестику")
    def test_close_ingredient_modal_by_cross(self, driver):
        main_page = MainPage(driver)

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Открываем модальное окно ингредиента"):
            main_page.click_first_ingredient()
            assert main_page.is_ingredient_modal_open(), \
                "Модальное окно не открылось — тест не может продолжаться"

        with allure.step("Закрываем модальное окно кликом по крестику"):
            main_page.close_ingredient_modal()

        with allure.step("Проверяем, что модальное окно закрылось"):
            assert main_page.is_ingredient_modal_closed(), \
                "Модальное окно не закрылось после клика по крестику"

    @allure.story("Счётчик ингредиента")
    @allure.title("[{driver}] Добавление ингредиента в заказ увеличивает счётчик")
    def test_add_ingredient_increases_counter(self, driver):
        main_page = MainPage(driver)

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Запоминаем начальное значение счётчика первого ингредиента"):
            counter_before = main_page.get_first_ingredient_counter()

        with allure.step("Добавляем первый ингредиент в конструктор"):
            main_page.add_first_ingredient()

        with allure.step("Проверяем, что счётчик увеличился"):
            counter_after = main_page.get_first_ingredient_counter()
            assert counter_after > counter_before, (
                f"Счётчик не увеличился: было {counter_before}, стало {counter_after}"
            )
