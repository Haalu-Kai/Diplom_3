from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import LONG_TIMEOUT
from pages.base_page import BasePage


class OrderModal(BasePage):
    """Модальное окно подтверждения / создания заказа."""

    # Пока заказ создаётся — крутилка с «9999» или «...»
    ORDER_LOADING = (By.XPATH, "//p[contains(@class,'Modal_modal') and text()='9999']")

    # Итоговый номер заказа (появляется после создания)
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class,'Modal_modal') and @class]")

    # Заголовок «Ваш заказ начали готовить»
    ORDER_CONFIRM_HEADER = (By.XPATH, "//p[text()='Ваш заказ начали готовить']")

    # Кнопка закрыть
    CLOSE_BTN = (
        By.XPATH,
        "//div[contains(@class,'Modal_modal__container')]"
        "//button[contains(@class,'Modal_modal__close')]"
    )

    def get_order_number(self, timeout=LONG_TIMEOUT) -> str:
        """
        Ждёт исчезновения крутилки и возвращает номер созданного заказа.
        Номер — строка с числом, например '12345'.
        """
        # Ждём, пока заглушка «9999» пропадёт
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ORDER_LOADING)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.ORDER_LOADING)
            )
        except Exception:
            pass

        # Ждём подтверждения и читаем номер
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ORDER_CONFIRM_HEADER)
        )
        number_el = self.find_visible(self.ORDER_NUMBER)
        return number_el.text.strip()

    def close(self):
        self.click(self.CLOSE_BTN)
