import requests
import logging
from settings.variables import API_URL, WORKSPACE, MY_FILES_SECTION, WORKFLOWS_SECTION

class GetFileListClient:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.url = API_URL

    def get_file_list(self) -> list[str]:
        payload = {
            "request": WORKSPACE,
            "action": "read",
            "fields": "recordId,link,name,type,recycled,isFolder",
            "section": MY_FILES_SECTION,
            "session": self.session_id
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(self.url, data=payload, headers=headers)

        response.raise_for_status()
        result = response.json()

        assert result.get("success") is True, f"Запрос завершился неудачно: {result}"

        raw_files = result.get("data", [])

        file_list = [
            f"{item['name']}.{item['type']}"
            for item in raw_files
            if str(item.get("isFolder", "true")).lower() == "false"
            if str(item.get("recycled", "true")).lower() == "false"
        ]
        return file_list

    def get_process_list(self) -> list[str]:
        payload = {
            "request": WORKSPACE,
            "action": "read",
            "fields": "recordId,link,name,type,recycled,isFolder",
            "section": WORKFLOWS_SECTION,
            "session": self.session_id
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(self.url, data=payload, headers=headers)

        response.raise_for_status()
        result = response.json()

        assert result.get("success") is True, f"Запрос завершился неудачно: {result}"

        raw_files = result.get("data", [])

        file_list = [
            f"{item['name']}.{item['type']}"
            for item in raw_files
            if str(item.get("isFolder", "true")).lower() == "false"
            if str(item.get("recycled", "true")).lower() == "false"
        ]
        return file_list
