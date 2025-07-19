import requests
from settings.variables import API_URL

class AuthClient:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.url = API_URL

    def get_session(self) -> str:
        payload = {
            "request": "signin",
            "login": self.login,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(self.url, data=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        assert data.get("session"), "Сессия отсутствует в ответе"
        assert data.get("success") is True, "Авторизация неуспешна"

        session_id = data["session"]

        return session_id