import requests
from pathlib import Path
from settings.variables import API_URL, WORKSPACE, UPLOADS_PATH, MY_FILES_SECTION

class FileUploadClient:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.url = API_URL
        self.UPLOADS_PATH = UPLOADS_PATH
    
    def upload_file(self, file_name: str):
        file_path = Path(UPLOADS_PATH) / file_name
        if not Path(file_path).is_file():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        payload = {
            "request": WORKSPACE,
            "action": "content",
            "method": "create",
            "folder": "00000000-0000-0000-0000-000000000000",
            "section": MY_FILES_SECTION,
            "session": self.session_id
        }

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(self.url, data=payload, files=files)

        response.raise_for_status()
        result = response.json()

        assert result.get("success") is True, f"Загрузка не удалась: {result}"
        try:
            record_id = result["data"][0]["recordId"]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"recordId не найден в ответе: {result}") from e

        return record_id