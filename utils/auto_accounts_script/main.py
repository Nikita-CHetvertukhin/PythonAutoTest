# main.py
import os
import sys
import argparse
import logging
import json
from pathlib import Path

import yaml
from dotenv import load_dotenv

from doczilla_client import DoczillaClient

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Настройка пользователей в Doczilla")
    parser.add_argument("--debug", action="store_true", help="Включить отладочный режим")
    parser.add_argument("--reset-password", action="store_true", help="Сбрасывать пароль перед установкой")
    parser.add_argument("--config", default="config.yaml", help="Путь к файлу конфигурации (по умолчанию: config.yaml)")
    parser.add_argument("--env", default=".env", help="Путь к .env файлу (по умолчанию: .env)")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    env_path = Path(args.env)
    if not env_path.exists():
        logger.error(f".env файл не найден: {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    config = load_config(args.config)

    base_url = os.getenv("DOCZILLA_URL")
    owner_login = os.getenv("OWNER_LOGIN")
    owner_password = os.getenv("OWNER_PASSWORD")

    if not all([base_url, owner_login, owner_password]):
        logger.error("Не заданы обязательные переменные в .env: DOCZILLA_URL, OWNER_LOGIN, OWNER_PASSWORD")
        sys.exit(1)

    client = DoczillaClient(base_url, owner_login, owner_password)
    client.authenticate()

    # --- Группа ---
    group_name = config["group"]["name"]
    group_id = client.group_exists(group_name)
    if not group_id:
        group_id = client.create_group(group_name)

    # --- Пользователи ---
    role_sets = config["role_sets"]
    entry_sets = config["entry_sets"]

    for user in config["users"]:
        login = user["login"]
        password = user["password"]
        user_type = user["type"]

        user_id = client.user_exists(login)
        is_new = user_id is None
        if is_new:
            user_id = client.create_user(login)
        else:
            # Очистка существующих связей
            client.clear_user_roles(user_id)
            client.clear_user_entries(user_id)
            client.clear_user_groups(user_id)
            if args.reset_password:
                client.reset_password(user_id)

        # Назначение группы
        client.assign_group(user_id, group_id)

        # Разрешение ролей и компонентов
        role_names = role_sets[user_type]
        entry_names = entry_sets[user_type]

        role_ids = client.resolve_role_ids(role_names)
        entry_ids = client.resolve_entry_ids(entry_names)

        client.assign_roles(user_id, role_ids)
        client.assign_entries(user_id, entry_ids)

        # Установка пароля
        client.set_password(login, password)

    logger.info("Настройка пользователей завершена успешно!")


if __name__ == "__main__":
    main()