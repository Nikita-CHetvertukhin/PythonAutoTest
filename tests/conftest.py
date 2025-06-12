#Глобальный импорт
import pytest
import os
import json
import time
import sys
#Локальный импорт
from utils.browser_driver import BrowserDriver
from utils.exception_handler.configure_logging import configure_logging
from utils.exception_handler.error_handler import ErrorHandler
from utils.element_searching import XPathFinder
from pages.login_page import LoginPage
from locators.base_locators import BaseLocators
from settings.variables import ADMIN_LOGIN, ADMIN_PASSWORD, URL, USER1_LOGIN, USER1_PASSWORD

# Пути к файлам
DEFAULT_LICENCE_FILE = "settings/default_licence_properties.json"
LICENCE_OUTPUT_FILE = "log/licence_properties.json"
ENV_FILE = "allure_results/environment.properties"

@pytest.fixture(scope="function")
def driver():
    """Создание нового драйвера для каждого теста"""
    driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome"))
    driver = driver_instance.initialize_driver()

    yield driver  # Передаём драйвер в тесты

    driver_instance.cleanup()  # Закрываем браузер после теста

@pytest.fixture(scope="session")
def logger():
    """
    Фикстура для логгера, который будет использоваться в тестах.
    """
    return configure_logging()

@pytest.fixture(scope="function")
def error_handler(driver, logger):
    """
    Фикстура для инициализации ErrorHandler с использованием driver и logger.
    """
    return ErrorHandler(driver, logger)

@pytest.fixture(scope="function")
def admin_driver(driver, logger, error_handler):
    """Создаёт новый браузер и выполняет авторизацию"""
    login_page = LoginPage(driver, logger)

    login_page.enter_username(ADMIN_LOGIN)
    login_page.enter_password(ADMIN_PASSWORD)
    login_page.click_login()

    assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
    time.sleep(3)  # Доработать в будущем

    return driver  # Передаём браузер без закрытия (его закроет driver)

@pytest.fixture(scope="function")
def user1_driver(logger, error_handler):
    """Создаёт новый браузер и выполняет авторизацию"""
    driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome").strip())
    driver = driver_instance.initialize_driver()
    login_page = LoginPage(driver, logger)

    login_page.enter_username(USER1_LOGIN)
    login_page.enter_password(USER1_PASSWORD)
    login_page.click_login()

    assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
    time.sleep(3)  # Доработать в будущем

    yield driver  # Передаём драйвер в тесты

    driver_instance.cleanup()  # Закрываем браузер после теста

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Формирует Licence_Properties. Добавляет сведения о браузере, url и лицензиях в отчет allure"""
    """Запускаем хук только если pytest вызван с `tests/check_url`."""
    command_line_args = sys.argv  # Получаем аргументы запуска pytest

    # Проверяем, что команда - содержит аргумент `tests/check_url`
    if "tests/check_url" in command_line_args:
        print("Запускаем проверку лицензий")
        if not hasattr(config, 'workerinput'):  # Проверяем, не является ли это воркером xdist
            os.makedirs("log", exist_ok=True)
            os.makedirs("log/screenshots", exist_ok=True)
            os.makedirs("allure_results", exist_ok=True)
            os.makedirs("allure_reports", exist_ok=True)
            os.makedirs("resources/downloads", exist_ok=True)
            os.makedirs("resources/uploads", exist_ok=True)

            driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome"))
            driver = driver_instance.initialize_driver()

            xpath = XPathFinder(driver)
            script_element = xpath.find_located(BaseLocators.LICENCE_PROPERTIES, timeout=10)
            script_text = script_element.get_attribute("innerText").strip()

            json_str = script_text.replace("Licence.Properties=", "").rstrip(";").strip()

            try:
                current_licence = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Ошибка JSON-декодирования: {e}")
                current_licence = {}

            driver.quit()
            driver_instance.cleanup()  # Удаляем временные файлы после работы

            with open(DEFAULT_LICENCE_FILE, "r", encoding="utf-8") as file:
                default_licence = json.load(file)

            merged_licence = {key: current_licence.get(key, default_licence[key]) for key in default_licence}

            with open(LICENCE_OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(merged_licence, file, indent=4)

            with open(DEFAULT_LICENCE_FILE, "r", encoding="utf-8") as file:
                default_licence = json.load(file)

            with open(LICENCE_OUTPUT_FILE, "r", encoding="utf-8") as file:
                current_licence = json.load(file)

            # Определяем отличающиеся параметры
            diff_licence = {
                key: value for key, value in current_licence.items()
                if default_licence.get(key) != value
            }

            # Открываем `environment.properties` один раз и записываем всё сразу
            with open(ENV_FILE, "w", encoding="utf-8") as file:
                file.write(f"URL={URL}\n")
                file.write(f'Browser={os.getenv("BROWSER")}\n')

                # Записываем только отличающиеся параметры
                for key, value in diff_licence.items():
                    file.write(f"{key}={value}\n")

                # В конце добавляем путь к файлу с полным списком лицензий
                file.write(f"Licence.Properties={LICENCE_OUTPUT_FILE}\n")
        if hasattr(config, 'workerinput'):
            return  # Не вызываем pytest.exit() на воркерах
    else:
         licence_file = os.path.join("log", "licence_properties.json")  # Путь к файлу лицензий
         if not os.path.exists(licence_file):
             pytest.exit("Файл licence_properties.json отсутствует! Запустите `pytest tests/check_url` для его формирования.")
         else:
            print("Пропускаем проверку лицензий, лицензии сформированы")
