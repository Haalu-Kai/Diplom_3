# Stellar Burgers — UI тесты (Задание 3)

## Структура проекта

```
stellar_burgers_ui/
├── config.py                        # URL, эндпоинты, таймауты
├── conftest.py                      # Фикстуры: driver (Chrome+Firefox), new_user, logged_in_driver
├── pytest.ini                       # Настройки pytest + alluredir
├── requirements.txt
├── utils/
│   └── helpers.py                   # Генерация данных, API-методы регистрации/удаления
├── pages/                           # Page Object Model
│   ├── base_page.py                 # Базовый класс с методами ожидания
│   ├── main_page.py                 # Главная страница / Конструктор
│   ├── login_page.py                # Страница входа
│   ├── order_feed_page.py           # Лента заказов
│   └── order_modal_page.py          # Модалка создания заказа
└── tests/
    ├── test_main_functionality.py   # Основная функциональность (5 тестов)
    └── test_order_feed.py           # Лента заказов (3 теста)
```

## Покрытые сценарии

### Основная функциональность (test_main_functionality.py)
| Тест | Описание |
|---|---|
| `test_click_constructor_nav_opens_constructor` | Переход по клику на «Конструктор» |
| `test_click_order_feed_nav_opens_order_feed` | Переход по клику на «Лента заказов» |
| `test_click_ingredient_opens_modal` | Клик по ингредиенту открывает модальное окно |
| `test_close_ingredient_modal_by_cross` | Модальное окно закрывается кликом по крестику |
| `test_add_ingredient_increases_counter` | Добавление ингредиента увеличивает счётчик |

### Лента заказов (test_order_feed.py)
| Тест | Описание |
|---|---|
| `test_new_order_increases_all_time_counter` | Счётчик «Выполнено за всё время» увеличивается |
| `test_new_order_increases_today_counter` | Счётчик «Выполнено за сегодня» увеличивается |
| `test_new_order_appears_in_progress` | Номер заказа появляется в разделе «В работе» |

Каждый тест запускается **в Chrome и в Firefox** — итого 16 тестовых кейсов.

## Установка

### 1. Зависимости Python
```bash
pip install -r requirements.txt
```

### 2. Браузеры
- **Chrome**: скачать с https://www.google.com/chrome/
- **Firefox**: скачать с https://www.mozilla.org/firefox/

Драйверы (`chromedriver`, `geckodriver`) устанавливаются автоматически через `webdriver-manager`.

### 3. Allure CLI (для отчётов)
- macOS: `brew install allure`
- Windows: [инструкция](https://allurereport.org/docs/install-for-windows/)
- Linux: [инструкция](https://allurereport.org/docs/install-for-linux/)

## Запуск

### Запуск всех тестов (Chrome + Firefox)
```bash
pytest --alluredir=allure-results
```

### Только Chrome
```bash
pytest -k "chrome" --alluredir=allure-results
```

### Только Firefox
```bash
pytest -k "firefox" --alluredir=allure-results
```

### Конкретный файл
```bash
pytest tests/test_main_functionality.py --alluredir=allure-results
```

### Просмотр Allure-отчёта
```bash
allure serve allure-results
```

## Архитектурные решения

- **Page Object Model** — каждая страница — отдельный класс в `pages/`.
- **BasePage** — все ожидания (`WebDriverWait`) инкапсулированы в базовом классе; тесты не работают с `find_element` напрямую.
- **Параметризация браузеров** — фикстура `driver` параметризована через `params=["chrome", "firefox"]`, что означает автоматический запуск каждого теста дважды.
- **Изоляция** — фикстура `new_user` создаёт уникального пользователя через API и удаляет его после теста, не оставляя мусора.
- **Allure-шаги** — каждое действие обёрнуто в `allure.step`, отчёт читается как спецификация.
