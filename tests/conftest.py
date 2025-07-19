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
from settings.variables import *
from pages.my_tasks_page import MyTasksPage
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage
from pages.my_files_editor_page import MyFilesEditorPage
from pages.my_files_page import MyFilesPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import WEBSOCKET_PATCH, DEFAULT_LICENCE_FILE, LICENCE_OUTPUT_FILE, ENV_FILE
from api.auth_client import AuthClient
from api.upload_client import FileUploadClient
from api.rename_client import RenameClient
from utils.lists import split_files_by_extension, get_missing_files

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
def user1_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    is_combo_test = request.node.get_closest_marker("combo") is not None

    if is_combo_test:
        driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome").strip())
        user_driver = driver_instance.initialize_driver()
        error_handler = ErrorHandler(user_driver, logger)
        login_page = LoginPage(user_driver, logger)

        login_page.enter_username(USER1_LOGIN)
        login_page.enter_password(USER1_PASSWORD)
        login_page.click_login()
        assert login_page.check_account_button(), "Авторизация не удалась."
        error_handler.clear_browser_logs()
        time.sleep(3)  # В будущем замена на WebDriverWait

        yield user_driver
        driver_instance.cleanup()

    else:
        error_handler = ErrorHandler(driver, logger)
        login_page = LoginPage(driver, logger)

        login_page.enter_username(USER1_LOGIN)
        login_page.enter_password(USER1_PASSWORD)
        login_page.click_login()
        assert login_page.check_account_button(), "Авторизация не удалась."
        error_handler.clear_browser_logs()
        time.sleep(3)

        yield driver

@pytest.fixture(scope="function")
def expert_driver(request, driver, logger):
    """Создаёт новый браузер и выполняет авторизацию"""
    is_combo_test = request.node.get_closest_marker("combo") is not None

    if is_combo_test:
        driver_instance = BrowserDriver(browser_type=os.getenv("BROWSER", "chrome").strip())
        driver = driver_instance.initialize_driver()
        error_handler = ErrorHandler(driver, logger)
        login_page = LoginPage(driver, logger)

        login_page.enter_username(EXPERT_LOGIN)
        login_page.enter_password(EXPERT_PASSWORD)
        login_page.click_login()

        assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
        # Сбрасываем консоль браузера чтобы обрабатывать только новые ошибки
        error_handler.clear_browser_logs()
        time.sleep(3)  # Доработать в будущем
        yield driver  # Передаём драйвер в тесты
        driver_instance.cleanup()  # Закрываем браузер после теста
    else:
        error_handler = ErrorHandler(driver, logger)
        login_page = LoginPage(driver, logger)

        login_page.enter_username(EXPERT_LOGIN)
        login_page.enter_password(EXPERT_PASSWORD)
        login_page.click_login()

        assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
        # Сбрасываем консоль браузера чтобы обрабатывать только новые ошибки
        error_handler.clear_browser_logs()
        time.sleep(3)  # Доработать в будущем
        yield driver  # Передаём драйвер в тесты

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_task(request, error_handler, logger, admin_driver):
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
    task_type = params.get("task_type")
    from_file = params.get("from_file", False)
    
    skip_cleanup = params.get("skip_cleanup")

    # Создание задачи с учётом возможных параметров
    kwargs = {}
    if task_deadline:
        kwargs["deadline"] = task_deadline
    if task_description:
        kwargs["task_description"] = task_description
    if task_executor:
        kwargs["executor"] = task_executor
    if task_type:
        kwargs["task_type"] = task_type
    if from_file:
        kwargs["from_file"] = from_file

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
            time.sleep(1)  # TODO: заменить на ожидание состояния страницы
            if my_tasks_page.find_task_by_name(task_name):
                my_tasks_page.right_click_and_select_action(task_name, "Удалить")
                logger.info(f"Задача '{task_name}' удалена.")
            else:
                logger.warning(f"Задача '{task_name}' не найдена при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"))

    if not skip_cleanup:
        request.addfinalizer(cleanup)
    return task_name, my_tasks_page, xpath

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_process(request, error_handler, logger, admin_driver):
    workflows_page = WorkflowsPage(admin_driver, logger)
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    xpath = workflows_page.xpath

    test_name = request.node.name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generate_name = f"{test_name}_{timestamp}"

    # Чтение параметров
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    upload_file_name = params.get("upload_file_name")
    publishing = params.get("publishing")
    skip_cleanup = params.get("skip_cleanup")

    if upload_file_name:
        # Создание через API: Загрузка и переименование
        auth_client = AuthClient(login={ADMIN_LOGIN}, password={ADMIN_PASSWORD_MD5})
        session_id = auth_client.get_session()

        upload_client = FileUploadClient(session_id=session_id)
        record_id = upload_client.upload_file(upload_file_name)

        rename_client = RenameClient(session_id=session_id)
        process_name = rename_client.rename_by_recordid(record_id, generate_name)
    else:
        # Создание через UI
        process_name = generate_name
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        time.sleep(1)  # TODO: заменить на WebDriverWait
        workflows_page.create_process(process_name)

    # Проверка
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    if not workflows_page.find_process_by_name(process_name):
        pytest.fail(f"Процесс '{process_name}' не был создан/загружен или найден.")

    # Публикация процесса, если указано в параметрах
    if publishing:
        workflows_page.right_click_and_select_action(process_name, "Открыть")
        time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться
        workflow_editor_page.action_from_document("Опубликовать")
        time.sleep(2) # Пока не на что опираться в редакторе

    def cleanup():
        # Снятие с публикации (если указано в параметрах) и удаление процесса
        if publishing:
            logger.info(f"Снятие с публикации процесса '{process_name}'...")
            workflows_page.click_header_logo_button()
            refresh_and_wait(admin_driver, logger)
            workflows_page.find_click_header_menu("Рабочие процессы")
            workflows_page.find_click_side_menu("Шаблоны процессов")
            time.sleep(1)
            workflows_page.right_click_and_select_action(process_name, "Открыть")
            time.sleep(2)
            workflow_editor_page.action_from_document("Снять с публикации")
        try:
            logger.info(f"Удаление процесса '{process_name}'...")
            workflows_page.click_header_logo_button()
            refresh_and_wait(admin_driver, logger)
            workflows_page.find_click_header_menu("Рабочие процессы")
            workflows_page.find_click_side_menu("Шаблоны процессов")
            time.sleep(1)
            if workflows_page.find_process_by_name(process_name):
                workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
                logger.info(f"Процесс '{process_name}' удален.")
            else:
                logger.warning(f"Процесс '{process_name}' не найден при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"))

    if not skip_cleanup:
        request.addfinalizer(cleanup)
    return process_name, workflows_page, xpath

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_file(request, error_handler, logger, admin_driver):
    my_files_page = MyFilesPage(admin_driver, logger)
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    xpath = my_files_page.xpath

    test_name = request.node.name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generate_name = f"{test_name}_{timestamp}"

    # Чтение параметров
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    upload_file_name = params.get("upload_file_name")
    publishing = params.get("publishing")
    skip_cleanup = params.get("skip_cleanup")
    file_type = params.get("file_type")

    if upload_file_name:
        # Создание через API: Загрузка и переименование
        auth_client = AuthClient(login={ADMIN_LOGIN}, password={ADMIN_PASSWORD_MD5})
        session_id = auth_client.get_session()

        upload_client = FileUploadClient(session_id=session_id)
        record_id = upload_client.upload_file(upload_file_name)

        rename_client = RenameClient(session_id=session_id)
        file_name = rename_client.rename_by_recordid(record_id, generate_name)
    else:
        # Создание через UI
        file_name = generate_name
        my_files_page.click_header_logo_button()
        my_files_page.find_click_side_menu("Мои файлы")
        time.sleep(1)  # TODO: заменить на WebDriverWait
        my_files_page.create_file(file_name, file_type)

    # Проверка
    my_files_page.click_header_logo_button()
    my_files_page.find_click_side_menu("Мои файлы")
    time.sleep(2) # Ждем загрузки раздела (потом заменить на ожидание реквеста)
    if not my_files_page.find_file_by_name(file_name):
        pytest.fail(f"Процесс '{file_name}' не был создан/загружен или найден.")

    # Публикация процесса, если указано в параметрах
    if publishing:
        my_files_page.right_click_and_select_action(file_name, "Открыть")
        time.sleep(2)  # Ждем, пока откроется редактор. (потом заменить на ожидание статусов)
        # Пропишу когда займусь коробкой

    def cleanup():
        # Снятие с публикации (если указано в параметрах) и удаление файла
        if publishing:
            logger.info(f"Снятие с публикации шаблона '{file_name}'...")
            # Пропишу когда займусь коробкой
        try:
            logger.info(f"Удаление файла '{file_name}'...")
            my_files_page.click_header_logo_button()
            refresh_and_wait(admin_driver, logger)
            time.sleep(1)
            if my_files_page.find_file_by_name(file_name):
                my_files_page.right_click_and_select_action(file_name, "Переместить в Корзину")
                logger.info(f"Файл '{file_name}' удален.")
            else:
                logger.warning(f"Файл '{file_name}' не найден при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"))

    if not skip_cleanup:
        request.addfinalizer(cleanup)
    return file_name, my_files_page, xpath

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Формирует Licence_Properties. Добавляет сведения о браузере, url и лицензиях в отчет allure"""
    """Запускаем хук только если pytest вызван с `tests/check_url`."""
    command_line_args = sys.argv  # Получаем аргументы запуска pytest

    # Проверяем, что команда - содержит аргумент `tests/check_url` и формируем или ищем файл лицензий
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
            # logger.info("Запуск на воркере — загрузка не производится.")
            return
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