BASE_URL = "https://stellarburgers.education-services.ru"
API_URL = f"{BASE_URL}/api"

# API endpoints
REGISTER_URL = f"{API_URL}/auth/register"
LOGIN_URL = f"{API_URL}/auth/login"
DELETE_USER_URL = f"{API_URL}/auth/user"
INGREDIENTS_URL = f"{API_URL}/ingredients"
ORDERS_URL = f"{API_URL}/orders"

# URLs веб-приложения
MAIN_PAGE_URL = BASE_URL
LOGIN_PAGE_URL = f"{BASE_URL}/login"
ORDER_FEED_URL = f"{BASE_URL}/feed"

# Таймауты
DEFAULT_TIMEOUT = 15
LONG_TIMEOUT = 30
