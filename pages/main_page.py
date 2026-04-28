from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import MAIN_PAGE_URL, DEFAULT_TIMEOUT, LONG_TIMEOUT
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница — Конструктор бургеров."""

    # Навигация
    NAV_CONSTRUCTOR = (By.XPATH, "//p[text()='Конструктор']")
    NAV_ORDER_FEED = (By.XPATH, "//p[text()='Лента заказов']")

    # Заголовок конструктора (проверяем, что мы на главной)
    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[text()='Соберите бургер']")

    # Секции конструктора
    SECTION_BUNS = (By.XPATH, "//span[text()='Булки']")
    SECTION_SAUCES = (By.XPATH, "//span[text()='Соусы']")
    SECTION_FILLINGS = (By.XPATH, "//span[text()='Начинки']")

    # Список ингредиентов
    INGREDIENT_ITEMS = (By.XPATH, "//a[contains(@class,'BurgerIngredient_ingredient')]")

    # Первый ингредиент (булка)
    FIRST_INGREDIENT = (By.XPATH, "(//a[contains(@class,'BurgerIngredient_ingredient')])[1]")

    # Счётчик первого ингредиента
    FIRST_INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@class,'BurgerIngredient_ingredient')])[1]"
        "//p[contains(@class,'counter_counter__num')]"
    )

    # Кнопка «Добавить» у первого ингредиента
    FIRST_INGREDIENT_ADD_BTN = (
        By.XPATH,
        "(//a[contains(@class,'BurgerIngredient_ingredient')])[1]//button"
    )

    # Всплывающее окно детали ингредиента
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]")
    INGREDIENT_MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    INGREDIENT_MODAL_CLOSE_BTN = (
        By.XPATH,
        "//div[contains(@class,'Modal_modal__container')]"
        "//button[contains(@class,'Modal_modal__close')]"
    )

    # Корзина / конструктор бургера (область дропа)
    BURGER_CONSTRUCTOR = (By.XPATH, "//section[contains(@class,'BurgerConstructor_constructor')]")

    # Кнопка оформить заказ
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    def open_main_page(self):
        self.open(MAIN_PAGE_URL)
        self.find_visible(self.CONSTRUCTOR_HEADER)

    def click_constructor_nav(self):
        self.click(self.NAV_CONSTRUCTOR)

    def click_order_feed_nav(self):
        self.click(self.NAV_ORDER_FEED)

    def is_constructor_visible(self) -> bool:
        return self.is_visible(self.CONSTRUCTOR_HEADER)

    def click_first_ingredient(self):
        self.click(self.FIRST_INGREDIENT)

    def is_ingredient_modal_open(self) -> bool:
        return self.is_visible(self.INGREDIENT_MODAL_TITLE)

    def close_ingredient_modal(self):
        self.click(self.INGREDIENT_MODAL_CLOSE_BTN)

    def is_ingredient_modal_closed(self) -> bool:
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element_located(self.INGREDIENT_MODAL)
            )
            return True
        except Exception:
            return False

    def get_first_ingredient_counter(self) -> int:
        """Возвращает значение счётчика первого ингредиента (0 если счётчика нет)."""
        try:
            counter_el = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.FIRST_INGREDIENT_COUNTER)
            )
            return int(counter_el.text)
        except Exception:
            return 0

    def add_first_ingredient(self):
        """Кликает кнопку «Добавить» у первого ингредиента."""
        self.click(self.FIRST_INGREDIENT_ADD_BTN)

    def click_order_button(self):
        self.click(self.ORDER_BUTTON)
