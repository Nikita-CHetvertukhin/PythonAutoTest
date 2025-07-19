import requests
from settings.variables import API_URL, WORKSPACE, MY_FILES_SECTION


class RenameClient:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.url = API_URL

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

        response = requests.post(self.url, data=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        assert result.get(
            "success") is True, f"Переименование неуспешно: {result}"
        try:
            new_name = result["data"][0]["name"]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"name не найден в ответе: {result}") from e
        return new_name