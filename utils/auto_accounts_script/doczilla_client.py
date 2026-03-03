import re
import hashlib
import json
import logging
import requests
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class DoczillaClient:
    def __init__(self, base_url: str, owner_login: str, owner_password: str):
        self.base_url = base_url.rstrip("/")
        self.owner_login = owner_login
        self.owner_password = self._normalize_password(owner_password)
        self.session: Optional[str] = None
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def _normalize_password(self, pwd: str) -> str:
        """Принимает MD5 или plain password, возвращает MD5."""
        if re.fullmatch(r"[0-9a-fA-F]{32}", pwd):
            return pwd
        return hashlib.md5(pwd.encode("utf-8")).hexdigest()

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"POST {url} with data: {data}")
        try:
            response = requests.post(url, headers=self.headers, data=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Response: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise

    def authenticate(self):
        print(self.owner_login, " ", self.owner_password)
        payload = {
            "request": "signin",
            "login": self.owner_login,
            "password": self.owner_password,
        }
        resp = self._post("/request.json", payload)
        self.session = resp["session"]
        logger.info(f"Аутентификация успешна. Сессия: {self.session[:8]}...")

    # --- Работа с пользователями ---
    def user_exists(self, login: str) -> Optional[str]:
        filter_ = json.dumps([{"property": "login", "operator": "contains", "value": login}])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "read",
            "quickFilter": filter_,
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        data = resp.get("data", [])
        if data:
            record_id = data[0]["recordId"]
            logger.debug(f"Пользователь {login} найден: {record_id}")
            return record_id
        logger.debug(f"Пользователь {login} не найден")
        return None

    def create_user(self, login: str) -> str:
        data = json.dumps([{"recordId": "00000000-0000-0000-0000-000000000000", "login": login, "changePassword": "False"}])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "create",
            "data": data,
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        record_id = resp["data"][0]["recordId"]
        logger.info(f"Создан пользователь {login}: {record_id}")
        return record_id

    def reset_password(self, user_id: str):
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "action",
            "name": "resetPassword",
            "records": json.dumps([user_id]),
            "session": self.session,
        }
        self._post("/request.json", payload)
        logger.info(f"Пароль сброшен для пользователя {user_id}")

    def set_password(self, login: str, new_password: str):
        # Вход под пустым паролем (стандартный хэш пустой строки)
        empty_hash = "d41d8cd98f00b204e9800998ecf8427e"
        temp_session = self._get_temp_session(login, empty_hash)
        new_hash = hashlib.md5(new_password.encode("utf-8")).hexdigest()
        payload = {
            "request": "password",
            "login": login,
            "password": empty_hash,
            "newPassword": new_hash,
            "session": temp_session,
        }
        self._post("/request.json", payload)
        logger.info(f"Установлен пароль для пользователя {login}")

    def _get_temp_session(self, login: str, password_hash: str) -> str:
        payload = {
            "request": "signin",
            "login": login,
            "password": password_hash,
        }
        resp = self._post("/request.json", payload)
        return resp["session"]

    # --- Очистка связей ---
    def _clear_related_records(self, user_id: str, query: str, record_key: str, fields: str):
        filter_ = json.dumps([{"property": f"{query}.userId", "value": user_id}])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "read",
            "filter": filter_,
            "fields": fields,
            "query": query,
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        records = resp.get("data", [])
        if not records:
            return

        record_ids = [item[record_key] for item in records]
        data = [{record_key: rid} for rid in record_ids]
        destroy_payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "destroy",
            "data": json.dumps(data),
            "query": query,
            "session": self.session,
        }
        self._post("/request.json", destroy_payload)
        logger.debug(f"Очищено {len(record_ids)} записей в {query} для пользователя {user_id}")

    def clear_user_roles(self, user_id: str):
        self._clear_related_records(
            user_id,
            query="userRoles",
            record_key="userRoles.recordId",
            fields='["userRoles.role.name","userRoles.userId"]'
        )

    def clear_user_groups(self, user_id: str):
        self._clear_related_records(
            user_id,
            query="userGroups",
            record_key="userGroups.recordId",
            fields='["userGroups.group.login","userGroups.userId"]'
        )

    def clear_user_entries(self, user_id: str):
        self._clear_related_records(
            user_id,
            query="userEntries",
            record_key="userEntries.recordId",
            fields='["userEntries.entry.description","userEntries.position","userEntries.userId"]'
        )


    def get_all_entries(self) -> List[Dict[str, Any]]:
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "read",
            "query": "userEntries.entry",
            "fields": '["userEntries.entry.name","userEntries.entry.description","userEntries.entry.recordId"]',
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        return resp.get("data", [])

    def get_all_roles(self) -> List[Dict[str, Any]]:
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "read",
            "query": "userRoles.role",
            "fields": '["userRoles.role.name","userRoles.role.recordId"]',
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        return resp.get("data", [])

    def find_entry_id_by_name(self, name: str) -> Optional[str]:
        entries = self.get_all_entries()
        for e in entries:
            if e.get("userEntries.entry.name") == name:
                return e["userEntries.entry.recordId"]
            if e.get("userEntries.entry.description", "").split(" (")[0] == name:
                return e["userEntries.entry.recordId"]
        return None

    def resolve_entry_ids(self, names: List[str]) -> List[str]:
        entry_map = {}
        entries = self.get_all_entries()
        for e in entries:
            name1 = e.get("userEntries.entry.name")
            name2 = e.get("userEntries.entry.description", "").split(" (")[0]
            rid = e["userEntries.entry.recordId"]
            if name1:
                entry_map[name1] = rid
            if name2:
                entry_map[name2] = rid

        ids = []
        for name in names:
            rid = entry_map.get(name)
            if rid:
                ids.append(rid)
            else:
                logger.warning(f"Компонент не найден: {name}")


        doc_id = entry_map.get("Документы")
        if doc_id and doc_id not in ids:
            ids.append(doc_id)

        return ids

    def resolve_role_ids(self, names: List[str]) -> List[str]:
        role_map = {}
        roles = self.get_all_roles()
        for r in roles:
            name = r.get("userRoles.role.name")
            if name:
                role_map[name] = r["userRoles.role.recordId"]

        ids = []
        for name in names:
            rid = role_map.get(name)
            if rid:
                ids.append(rid)
            else:
                logger.warning(f"Роль не найдена: {name}")
        return ids


    def assign_entries(self, user_id: str, entry_ids: List[str]):
        for eid in entry_ids:
            data = json.dumps([{
                "userEntries.recordId": "00000000-0000-0000-0000-000000000000",
                "userEntries.userId": user_id,
                "userEntries.entryId": eid
            }])
            payload = {
                "request": "org.zenframework.z8.server.base.table.system.view.UserView",
                "action": "create",
                "data": data,
                "query": "userEntries",
                "session": self.session,
            }
            self._post("/request.json", payload)
        logger.info(f"Назначено {len(entry_ids)} компонентов пользователю {user_id}")

    def assign_roles(self, user_id: str, role_ids: List[str]):
        for rid in role_ids:
            data = json.dumps([{
                "userRoles.recordId": "00000000-0000-0000-0000-000000000000",
                "userRoles.userId": user_id,
                "userRoles.roleId": rid
            }])
            payload = {
                "request": "org.zenframework.z8.server.base.table.system.view.UserView",
                "action": "create",
                "data": data,
                "query": "userRoles",
                "session": self.session,
            }
            self._post("/request.json", payload)
        logger.info(f"Назначено {len(role_ids)} ролей пользователю {user_id}")


    def group_exists(self, login: str) -> Optional[str]:
        filter_ = json.dumps([{"property": "login", "operator": "contains", "value": login}])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserGroupView",
            "action": "read",
            "quickFilter": filter_,
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        data = resp.get("data", [])
        if data:
            return data[0]["recordId"]
        return None

    def create_group(self, login: str) -> str:
        data = json.dumps([{"recordId": "00000000-0000-0000-0000-000000000000", "login": login}])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserGroupView",
            "action": "create",
            "data": data,
            "session": self.session,
        }
        resp = self._post("/request.json", payload)
        record_id = resp["data"][0]["recordId"]
        logger.info(f"Создана группа {login}: {record_id}")
        return record_id

    def assign_group(self, user_id: str, group_id: str):
        data = json.dumps([{
            "userGroups.recordId": "00000000-0000-0000-0000-000000000000",
            "userGroups.userId": user_id,
            "userGroups.groupId": group_id
        }])
        payload = {
            "request": "org.zenframework.z8.server.base.table.system.view.UserView",
            "action": "create",
            "data": data,
            "query": "userGroups",
            "session": self.session,
        }
        self._post("/request.json", payload)
        logger.info(f"Пользователь {user_id} добавлен в группу {group_id}")