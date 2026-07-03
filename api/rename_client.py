import logging
import allure
from settings.variables import API_URL, WORKSPACE, MY_FILES_SECTION
from api.base_client import post_and_log

logger = logging.getLogger(__name__)


class RenameClient:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.url = API_URL

    @allure.step("Переименование файла с recordid = {record_id}; в {new_name} через API")
    def rename_by_recordid(self, record_id, new_name):
        payload = {
            "request": WORKSPACE,
            "action": "content",
            "method": "rename",
            "file": record_id,
            "name": new_name,
            "session": self.session_id
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = post_and_log(logger, self.url, data=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        assert result.get(
            "success") is True, f"Переименование неуспешно: {result}"
        try:
            new_name = result["data"][0]["name"]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"name не найден в ответе: {result}") from e
        return new_name