import random
import string
import requests

from config import REGISTER_URL, DELETE_USER_URL


def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_user_data():
    suffix = generate_random_string(8)
    return {
        "email": f"test_{suffix}@example.com",
        "password": f"pass_{suffix}",
        "name": f"User_{suffix}",
    }


def register_user(user_data: dict) -> dict:
    """Регистрирует пользователя через API, возвращает тело ответа."""
    response = requests.post(REGISTER_URL, json=user_data)
    response.raise_for_status()
    return response.json()


def delete_user(access_token: str):
    """Удаляет пользователя через API."""
    if access_token:
        requests.delete(DELETE_USER_URL, headers={"Authorization": access_token})
