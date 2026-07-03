import logging
import allure
from settings.variables import API_URL
from api.base_client import post_and_log

logger = logging.getLogger(__name__)

class AuthClient:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.url = API_URL

    def get_session(self) -> str:
        with allure.step(f"Получение сессии API для: '{self.login}'"):
            payload = {
                "request": "signin",
                "login": self.login,
                "password": self.password
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = post_and_log(logger, self.url, data=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            assert data.get("session"), "Сессия отсутствует в ответе"
            assert data.get("success") is True, "Авторизация неуспешна"

            session_id = data["session"]

            return session_id