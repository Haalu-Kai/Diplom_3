import time
import allure
import pytest
import requests

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.order_modal_page import OrderModal
from config import INGREDIENTS_URL, ORDERS_URL, LONG_TIMEOUT


def _get_ingredient_ids() -> list:
    """Получает два валидных ID ингредиента из API."""
    response = requests.get(INGREDIENTS_URL)
    response.raise_for_status()
    ingredients = response.json()["data"]
    # Берём булку (индекс 0) и любой соус (индекс 1)
    return [ingredients[0]["_id"], ingredients[1]["_id"]]


def _place_order_via_ui(driver, new_user) -> str:
    """
    Вспомогательная функция:
    логинит пользователя, добавляет ингредиенты и оформляет заказ через UI.
    Возвращает номер заказа в виде строки.
    """
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    order_modal = OrderModal(driver)

    login_page.open_login_page()
    login_page.login(new_user["email"], new_user["password"])
    main_page.find_visible(main_page.CONSTRUCTOR_HEADER)

    # Добавляем ингредиент (булку — первый элемент)
    main_page.add_first_ingredient()

    # Оформляем заказ
    main_page.click_order_button()

    # Получаем номер заказа из модалки
    order_number = order_modal.get_order_number()
    return order_number


@allure.epic("Stellar Burgers UI")
@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.story("Счётчики")
    @allure.title("[{driver}] Создание заказа увеличивает счётчик «Выполнено за всё время»")
    def test_new_order_increases_all_time_counter(self, driver, new_user):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Открываем ленту заказов и запоминаем счётчик «за всё время»"):
            order_feed_page.open_order_feed()
            counter_before = order_feed_page.get_counter_all_time()
            allure.attach(
                str(counter_before),
                name="Счётчик до заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Создаём новый заказ"):
            order_number = _place_order_via_ui(driver, new_user)
            allure.attach(
                order_number,
                name="Номер заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Возвращаемся на ленту заказов"):
            order_feed_page.open_order_feed()

        with allure.step("Ждём обновления счётчика (до 30 секунд)"):
            deadline = time.time() + LONG_TIMEOUT
            counter_after = counter_before
            while time.time() < deadline:
                counter_after = order_feed_page.get_counter_all_time()
                if counter_after > counter_before:
                    break
                time.sleep(1)
                driver.refresh()

            allure.attach(
                str(counter_after),
                name="Счётчик после заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверяем, что счётчик «Выполнено за всё время» увеличился"):
            assert counter_after > counter_before, (
                f"Счётчик 'за всё время' не увеличился: было {counter_before}, стало {counter_after}"
            )

    @allure.story("Счётчики")
    @allure.title("[{driver}] Создание заказа увеличивает счётчик «Выполнено за сегодня»")
    def test_new_order_increases_today_counter(self, driver, new_user):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Открываем ленту заказов и запоминаем счётчик «за сегодня»"):
            order_feed_page.open_order_feed()
            counter_before = order_feed_page.get_counter_today()
            allure.attach(
                str(counter_before),
                name="Счётчик до заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Создаём новый заказ"):
            order_number = _place_order_via_ui(driver, new_user)

        with allure.step("Возвращаемся на ленту заказов"):
            order_feed_page.open_order_feed()

        with allure.step("Ждём обновления счётчика (до 30 секунд)"):
            deadline = time.time() + LONG_TIMEOUT
            counter_after = counter_before
            while time.time() < deadline:
                counter_after = order_feed_page.get_counter_today()
                if counter_after > counter_before:
                    break
                time.sleep(1)
                driver.refresh()

            allure.attach(
                str(counter_after),
                name="Счётчик после заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверяем, что счётчик «Выполнено за сегодня» увеличился"):
            assert counter_after > counter_before, (
                f"Счётчик 'за сегодня' не увеличился: было {counter_before}, стало {counter_after}"
            )

    @allure.story("Заказ в работе")
    @allure.title("[{driver}] После оформления заказа его номер появляется в разделе «В работе»")
    def test_new_order_appears_in_progress(self, driver, new_user):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Создаём новый заказ"):
            order_number = _place_order_via_ui(driver, new_user)
            allure.attach(
                order_number,
                name="Номер заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Открываем ленту заказов"):
            order_feed_page.open_order_feed()

        with allure.step(f"Ждём появления заказа #{order_number} в разделе «В работе»"):
            appeared = order_feed_page.wait_for_order_in_progress(order_number)

        with allure.step("Проверяем, что номер заказа отображается в «В работе»"):
            in_progress = order_feed_page.get_in_progress_order_numbers()
            allure.attach(
                str(in_progress),
                name="Заказы в работе",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert appeared or any(order_number in num for num in in_progress), (
                f"Заказ #{order_number} не появился в разделе 'В работе'. "
                f"Текущие заказы в работе: {in_progress}"
            )
