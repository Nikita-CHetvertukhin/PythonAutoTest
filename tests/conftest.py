#Глобальный импорт
import pytest
import os
import json
import time
import datetime
import sys
import glob
#Локальный импорт
from utils.browser_driver import BrowserDriver
from utils.exception_handler.configure_logging import configure_logging
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from utils.exception_handler.error_handler import ErrorHandler
from utils.element_searching import XPathFinder
from pages.login_page import LoginPage
from locators.base_locators import BaseLocators
from settings.variables import ADMIN_LOGIN, ADMIN_PASSWORD, URL, USER1_LOGIN, USER1_PASSWORD

# Пути к файлам
DEFAULT_LICENCE_FILE = "settings/default_licence_properties.json"
LICENCE_OUTPUT_FILE = "log/licence_properties.json"
ENV_FILE = "allure_results/environment.properties"
WEBSOCKET_PATCH = """
window.WebSocket = class {
  constructor() {
    console.warn("WebSocket блокирован: соединение не устанавливается.");
    this.readyState = 3; // CLOSED
  }
  close() {}
  send() {}
  set onopen(_) {}
  set onmessage(_) {}
  set onerror(_) {}
  set onclose(_) {}
};
"""

@pytest.fixture(scope="function")
def driver():
    """Создание нового драйвера для каждого теста"""
    driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome"))
    driver = driver_instance.initialize_driver()

    yield driver  # Передаём драйвер в тесты

    driver_instance.cleanup()  # Закрываем браузер после теста

@pytest.fixture(scope="function")
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

    driver.execute_script(WEBSOCKET_PATCH) # Отключаем вебсокеты для повышения стабильности тестов в ФС

    login_page.enter_username(ADMIN_LOGIN)
    login_page.enter_password(ADMIN_PASSWORD)
    login_page.click_login()

    assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
    # Сбрасываем консоль браузера чтобы обрабатывать только новые ошибки
    error_handler.clear_browser_logs()
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
    # Сбрасываем консоль браузера чтобы обрабатывать только новые ошибки
    error_handler.clear_browser_logs()
    time.sleep(3)  # Доработать в будущем

    yield driver  # Передаём драйвер в тесты

    driver_instance.cleanup()  # Закрываем браузер после теста

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_task(request, error_handler, logger, admin_driver):
    from pages.my_tasks_page import MyTasksPage
    from utils.refresh_and_wait import refresh_and_wait

    my_tasks_page = MyTasksPage(admin_driver, logger)
    xpath = my_tasks_page.xpath

    test_name = request.node.name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    task_name = f"{test_name}_{timestamp}"

    logger.info(f"Создание задачи '{task_name}' из теста '{test_name}'")

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1)  # TODO: заменить на ожидание состояния страницы

    # Извлекаем параметр deadline, если передан
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    task_deadline = params.get("deadline")
    task_description = params.get("description")
    task_executor = params.get("task_executor")

    # Создание задачи с учётом возможных параметров
    kwargs = {}
    if task_deadline:
        kwargs["deadline"] = task_deadline
    if task_description:
        kwargs["task_description"] = task_description
    if task_executor:
        kwargs["executor"] = task_executor

    my_tasks_page.create_task(task_name, **kwargs)

    if not my_tasks_page.find_task_by_name(task_name):
        pytest.fail(f"Задача '{task_name}' не была создана или найдена.")

    def cleanup():
        try:
            logger.info(f"Удаление задачи '{task_name}'...")
            my_tasks_page.click_header_logo_button()
            refresh_and_wait(admin_driver, logger)
            my_tasks_page.find_click_header_menu("Мои задачи")
            my_tasks_page.find_click_side_menu("Мои задачи")
            if my_tasks_page.find_task_by_name(task_name):
                my_tasks_page.right_click_and_select_action(task_name, "Удалить")
                logger.info(f"Задача '{task_name}' удалена.")
            else:
                logger.warning(f"Задача '{task_name}' не найдена при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"))

    request.addfinalizer(cleanup)
    return task_name, my_tasks_page, xpath

@pytest.fixture(scope="function")
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def setup_create_task(request, error_handler, logger, admin_driver):
    from pages.my_tasks_page import MyTasksPage

    my_tasks_page = MyTasksPage(admin_driver, logger)
    xpath = my_tasks_page.xpath

    # Получаем имя теста
    test_name = request.node.name  # Например: test_open_task_with_context_menu
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    task_name = f"{test_name}_{timestamp}"

    logger.info(f"Создание задачи '{task_name}' из теста '{test_name}'")

    # Логика создания
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1) # Ждем, чтобы страница успела загрузиться. Потом поправить на ожидание request
    my_tasks_page.create_task(task_name)

    if not my_tasks_page.find_task_by_name(task_name):
        pytest.fail(f"Задача '{task_name}' не была создана или найдена.")

    return task_name, my_tasks_page, xpath

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

def pytest_sessionfinish(session, exitstatus):
    args = session.config.invocation_params.args

    test_path = next((arg for arg in args if arg.startswith("tests/")), None)
    if test_path:
        print(f"Путь до тестов: {test_path}")
        # Берём последнюю часть пути как имя
        log_name = os.path.basename(test_path.strip("/\\"))
        merged_log_path = f"log/{log_name}.log"
    else:
        merged_log_path = "log/merged.log"  # fallback, если путь не найден

    should_merge_logs = False
    if "-n" in args:
        try:
            index = args.index("-n")
            value = args[index + 1]
            if value == "auto" or (value.isdigit() and int(value) > 1):
                should_merge_logs = True
        except (IndexError, ValueError):
            pass

    if should_merge_logs:
        print("Множественные воркеры — выполняем склейку логов...")

        log_files = glob.glob("log/project_*.log")
        if log_files:
            with open(merged_log_path, "w", encoding="utf-8") as merged:
                for f in log_files:
                    with open(f, "r", encoding="utf-8") as part:
                        merged.write(part.read())
            for f in log_files:
                os.remove(f)
            print(f"Логи из {len(log_files)} файлов объединены в {merged_log_path}")
        else:
            print("Не найдено логов для склейки")