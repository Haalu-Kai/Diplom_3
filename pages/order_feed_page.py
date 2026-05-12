from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import ORDER_FEED_URL, DEFAULT_TIMEOUT, LONG_TIMEOUT
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    """Страница «Лента заказов»."""

    PAGE_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")

    # Счётчики
    COUNTER_ALL_TIME = (
        By.XPATH,
        "//p[text()='Выполнено за всё время:']/following-sibling::p[contains(@class,'OrderFeed_number')]"
    )
    COUNTER_TODAY = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class,'OrderFeed_number')]"
    )

    # Секция «В работе»
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class,'OrderFeed_orderListReady')]")
    IN_PROGRESS_NUMBERS = (
        By.XPATH,
        "//ul[contains(@class,'OrderFeed_orderListReady')]/li"
    )

    def open_order_feed(self):
        self.open(ORDER_FEED_URL)
        self.find_visible(self.PAGE_HEADER)

    def is_order_feed_visible(self) -> bool:
        return self.is_visible(self.PAGE_HEADER)

    def get_counter_all_time(self) -> int:
        text = self.get_text(self.COUNTER_ALL_TIME)
        return int(text.replace('\u00a0', '').replace(' ', ''))

    def get_counter_today(self) -> int:
        text = self.get_text(self.COUNTER_TODAY)
        return int(text.replace('\u00a0', '').replace(' ', ''))

    def get_in_progress_order_numbers(self) -> list[str]:
        """Возвращает список номеров заказов из раздела «В работе»."""
        try:
            elements = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located(self.IN_PROGRESS_NUMBERS)
            )
            return [el.text.strip() for el in elements if el.text.strip()]
        except Exception:
            return []

    def wait_for_order_in_progress(self, order_number: str, timeout=LONG_TIMEOUT) -> bool:
        """Ждёт, пока номер заказа появится в разделе «В работе»."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(self.IN_PROGRESS_SECTION, order_number)
            )
            return True
        except Exception:
            return False
