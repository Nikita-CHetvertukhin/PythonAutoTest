#Глобальный импорт
import pytest
import os
import json
import time
import datetime
import sys
import glob
import re
import allure
import shutil
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
from utils.get_date import get_timestamp, get_uuid
from settings.variables import WEBSOCKET_PATCH, DEFAULT_LICENCE_FILE, LICENCE_OUTPUT_FILE, ENV_FILE
from api.auth_client import AuthClient
from api.upload_client import FileUploadClient
from api.rename_client import RenameClient

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузеры через запятую: chrome,firefox,edge или all"
    )

def pytest_generate_tests(metafunc):
    if "browser_type" in metafunc.fixturenames:
        raw = metafunc.config.getoption("browser")
        browsers = [b.strip().lower() for b in raw.split(",")]

        if "all" in browsers:
            browsers = ["chrome", "firefox", "edge"]

        # Убираем дубликаты
        # browsers = list(dict.fromkeys(browsers))
        if metafunc.function.__name__ == "test_generateDatabaseSchema":
            browsers = [browsers[0]]

        print(f"Параметры browser_type: {browsers}")
        metafunc.parametrize("browser_type", browsers)

@pytest.fixture(scope="function")
def driver(browser_type):
    """Создание драйвера с параметризацией браузера"""
    driver_instance = BrowserDriver(browser_type=browser_type)
    driver = driver_instance.initialize_driver()

    try:
        yield driver
    finally:
        driver_instance.cleanup()

@pytest.fixture(scope="function")
def logger():
    """
    Фикстура для логгера, который будет использоваться в тестах.
    """
    return configure_logging()

@pytest.fixture(scope="function")
def error_handler(driver, logger, browser_type):
    """
    Фикстура для инициализации ErrorHandler с использованием driver и logger.
    """
    return ErrorHandler(driver, logger, browser_type)

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

    return driver  # Передаём браузер без закрытия (его закроет driver)

@pytest.fixture(scope="function")
def expert_driver(request, driver, logger):
    """Создаёт новый браузер и выполняет авторизацию"""
    yield from login_user(request, driver, logger, EXPERT_LOGIN, EXPERT_PASSWORD)

@pytest.fixture(scope="function")
def user1_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    yield from login_user(request, driver, logger, USER1_LOGIN, USER1_PASSWORD)

@pytest.fixture(scope="function")
def user2_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    yield from login_user(request, driver, logger, USER2_LOGIN, USER2_PASSWORD)

@pytest.fixture(scope="function")
def user3_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    yield from login_user(request, driver, logger, USER3_LOGIN, USER3_PASSWORD)

@pytest.fixture(scope="function")
def user4_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    yield from login_user(request, driver, logger, USER4_LOGIN, USER4_PASSWORD)

@pytest.fixture(scope="function")
def user5_driver(request, driver, logger):
    """Создаёт новый браузер или наследует существующий — в зависимости от контекста теста."""
    yield from login_user(request, driver, logger, USER5_LOGIN, USER5_PASSWORD)

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_task(request, error_handler, logger, admin_driver):
    my_tasks_page = MyTasksPage(admin_driver, logger)
    xpath = my_tasks_page.xpath

    test_name = request.node.name.split("[")[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    task_name = f"{test_name}_{get_uuid()}_{timestamp}"

    logger.info(f"Создание задачи '{task_name}' из теста '{test_name}'")

    # Извлекаем параметр deadline, если передан
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    task_deadline = params.get("deadline")
    task_description = params.get("description")
    task_executor = params.get("task_executor")
    task_executors = params.get("task_executors")
    executors_massive = params.get("executors_massive")
    task_type = params.get("task_type")
    from_file = params.get("from_file", False)
    attache_file = params.get("attache_file")
    custom_task_name = params.get("task_name")
    if custom_task_name:
        task_name = custom_task_name

    def cleanup():
        try:
            logger.info(f"Очистка: попытка удалить задачу '{task_name}'...")
            my_tasks_page.click_header_logo_button()
            my_tasks_page.find_click_header_menu("Мои задачи")
            my_tasks_page.find_click_side_menu("Мои задачи")

            if my_tasks_page.find_file_by_name(task_name):
                try:
                    my_tasks_page.right_click_and_select_action(task_name, "Удалить")
                    logger.info(f"Задача '{task_name}' успешно удалена.")
                except Exception as delete_error:
                    logger.error(f"Ошибка при удалении: {delete_error}")
                    error_handler.handle_exception(MinorIssue("Задача осталась и не удалось её удалить."), critical=False)
            else:
                logger.info(f"Задача '{task_name}' не найдена — возможно, удалена в теле теста.")
        except Exception as e:
            logger.error(f"Ошибка при очистке: {e}")
            error_handler.handle_exception(MinorIssue("Очистка провалилась, но тест пройден."), critical=False)

    request.addfinalizer(cleanup)

    if not from_file:
        my_tasks_page.find_click_header_menu("Мои задачи")
        my_tasks_page.find_click_side_menu("Мои задачи")

    # Создание задачи с учётом возможных параметров
    kwargs = {}
    if task_deadline:
        kwargs["deadline"] = task_deadline
    if task_description:
        kwargs["task_description"] = task_description
    if task_executor:
        kwargs["executor"] = task_executor
    if task_executors:
        kwargs["executors"] = task_executors
    if executors_massive:
        kwargs["executors_massive"] = executors_massive
    if task_type:
        kwargs["task_type"] = task_type
    if from_file:
        kwargs["from_file"] = from_file
    if attache_file:
        kwargs["attache_file"] = attache_file

    my_tasks_page.create_task(task_name, **kwargs)

    if not from_file:
        if not my_tasks_page.find_file_by_name(task_name):
            raise AssertionError(f"Задача '{task_name}' не была создана или найдена.")

    return task_name, my_tasks_page, xpath

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_process(request, error_handler, logger, admin_driver):
    workflows_page = WorkflowsPage(admin_driver, logger)
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    xpath = workflows_page.xpath

    test_name = request.node.name.split("[")[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    process_name = f"{test_name}_{get_uuid()}_{timestamp}"

    # Чтение параметров
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    upload_file_name = params.get("upload_file_name")
    publishing = params.get("publishing")
    # Специальная логика для выбора каталога в автоматизациях
    shape_name = params.get("shape_name")
    type_auto = params.get("type_auto")
    type_section = params.get("type_section")
    name_catalog = params.get("name_catalog")
    custom_name = params.get("process_name")
    box_name = params.get("box_name")
    if custom_name:
        process_name = custom_name
    unique_check = params.get("unique_check", False)
    
    def cleanup():
        # Снятие с публикации (если указано в параметрах) и удаление процесса
        if publishing:
            logger.info(f"Снятие с публикации процесса '{process_name}'...")
            workflows_page.click_header_logo_button()
            workflows_page.find_click_header_menu("Рабочие процессы")
            workflows_page.find_click_side_menu("Шаблоны процессов")
            workflows_page.right_click_and_select_action(process_name, "Открыть")
            time.sleep(2) # TODO заменить на ожидание реквеста
            workflow_editor_page.action_from_document("Снять с публикации")
        try:
            logger.info(f"Удаление процесса '{process_name}'...")
            workflows_page.click_header_logo_button()
            workflows_page.find_click_header_menu("Рабочие процессы")
            workflows_page.find_click_side_menu("Шаблоны процессов")
            if workflows_page.find_file_by_name(process_name):
                workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
                logger.info(f"Процесс '{process_name}' удален.")
            else:
                logger.warning(f"Процесс '{process_name}' не найден при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"), critical=False)

    request.addfinalizer(cleanup)
    
    if unique_check:
        # Проверка на уникальность имени процесса
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        # Если файл с таким именем уже существует, то продолжаем работать с существующим
        if  workflows_page.find_file_by_name(process_name):
            return process_name, workflows_page, xpath
        else:
            # Если файл не найден, то продолжаем создание нового
            workflows_page.click_header_logo_button()

    if upload_file_name:
        # Создание через API: Загрузка и переименование
        auth_client = AuthClient(login={ADMIN_LOGIN}, password={ADMIN_PASSWORD_MD5})
        session_id = auth_client.get_session()

        upload_client = FileUploadClient(session_id=session_id)
        record_id = upload_client.upload_file(upload_file_name)

        rename_client = RenameClient(session_id=session_id)
        process_name = rename_client.rename_by_recordid(record_id, process_name)

        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
    else:
        # Создание через UI
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        workflows_page.create_process(process_name)

    # Проверка
    if not workflows_page.find_file_by_name(process_name):
        raise AssertionError(f"Процесс '{process_name}' не был создан/загружен или найден.")

    # Открытие процесса если переданы параметры натсреок внутри процесса
    if any([shape_name, publishing]):
        workflows_page.right_click_and_select_action(process_name, "Открыть")
        time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться
        workflow_editor_page.name_properties(name=process_name,action="set")

    # Установка пути источника для автоматизаций, если указано
    if type_section:
        workflow_editor_page.click_shape_by_text(text=shape_name)
        # Выбор каталога с учетом параметров
        kwargs = {}
        if type_auto:
            kwargs["type_auto"] = type_auto
        if type_section:
            kwargs["type_section"] = type_section
        if name_catalog:
            kwargs["name_catalog"] = name_catalog

        workflow_editor_page.change_catalog_in_auto(**kwargs)

    if box_name:
        workflow_editor_page.click_shape_by_text(text=shape_name)
        # Перевыбор УЗ в автоматизации
        kwargs = {}
        if type_auto:
            kwargs["type_auto"] = type_auto
        if box_name:
            kwargs["box_name"] = box_name

        workflow_editor_page.rechange_user_in_auto(**kwargs)

    # Публикация процесса, если указано в параметрах
    if publishing:
        workflow_editor_page.action_from_document("Опубликовать")
        time.sleep(2) # Пока не на что опираться в редакторе

    return process_name, workflows_page, xpath

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_file(request, error_handler, logger, admin_driver):
    my_files_page = MyFilesPage(admin_driver, logger)
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    xpath = my_files_page.xpath

    test_name = request.node.name.split("[")[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{test_name}_{get_uuid()}_{timestamp}"

    # Чтение параметров
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    upload_file_name = params.get("upload_file_name")
    publishing = params.get("publishing")
    file_type = params.get("file_type")
    custom_file_name = params.get("file_name")
    if custom_file_name:
        file_name = custom_file_name
    open_file = params.get("open_file", False)
    unique_check = params.get("unique_check", False)

    # Блок отвечает за очистку в любом случае после завершения теста
    def cleanup():
        # Снятие с публикации (если указано в параметрах) и удаление файла
        if publishing:
            logger.info(f"Снятие с публикации шаблона '{file_name}'...")
            # Пропишу когда займусь коробкой
        try:
            logger.info(f"Удаление файла '{file_name}'...")
            my_files_page.click_header_logo_button()
            my_files_page.find_click_header_menu("Документы")
            my_files_page.find_click_side_menu("Мои файлы")
            if my_files_page.find_file_by_name(file_name):
                my_files_page.right_click_and_select_action(file_name, "Переместить в Корзину")
                logger.info(f"Файл '{file_name}' удален.")
            else:
                logger.warning(f"Файл '{file_name}' не найден при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"), critical=False)
    
    request.addfinalizer(cleanup)
    
    if unique_check:
        # Проверка на уникальность имени файла
        my_files_page.find_click_header_menu("Документы")
        my_files_page.find_click_side_menu("Мои файлы")
        # Если файл с таким именем уже существует, то продолжаем работать с существующим
        if  my_files_page.find_file_by_name(file_name):
            return file_name, my_files_page, xpath
        else:
            # Если файл не найден, то продолжаем создание нового
            my_files_page.click_header_logo_button()

    if upload_file_name:
        # Создание через API: Загрузка и переименование
        auth_client = AuthClient(login={ADMIN_LOGIN}, password={ADMIN_PASSWORD_MD5})
        session_id = auth_client.get_session()

        upload_client = FileUploadClient(session_id=session_id)
        record_id = upload_client.upload_file(upload_file_name)

        rename_client = RenameClient(session_id=session_id)
        file_name = rename_client.rename_by_recordid(record_id, file_name)
        
        my_files_page.click_header_logo_button()
        my_files_page.find_click_header_menu("Документы")
        my_files_page.find_click_side_menu("Мои файлы")
    else:
        # Создание через UI
        my_files_page.click_header_logo_button()
        my_files_page.find_click_header_menu("Документы")
        my_files_page.find_click_side_menu("Мои файлы")
        my_files_page.create_file(file_name, file_type)

    # Проверка
    if open_file:
        my_files_page.right_click_and_select_action(file_name, "Открыть")
        time.sleep(2) # TODO Ждем загрузки раздела (потом заменить на ожидание реквеста)
    else:
        if not my_files_page.find_file_by_name(file_name):
            raise AssertionError(f"Файл '{file_name}' не был создан/загружен или найден.")

    # Публикация файла, если указано в параметрах
    if publishing:
        my_files_page.right_click_and_select_action(file_name, "Открыть")
        time.sleep(2)  # Ждем, пока откроется редактор. (потом заменить на ожидание статусов)
        # Пропишу когда займусь коробкой
    
    return file_name, my_files_page, xpath

@pytest.fixture(scope="function")
@exception_handler
def setup_create_delete_drive(request, error_handler, logger, admin_driver):
    my_files_page = MyFilesPage(admin_driver, logger)
    xpath = my_files_page.xpath

    test_name = request.node.name.split("[")[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    drive_name = f"{test_name}_{get_uuid()}_{timestamp}"
    # Извлекаем параметры из запроса, если они есть
    params = request.param if hasattr(request, "param") and isinstance(request.param, dict) else {}
    custom_drive_name = params.get("drive_name")
    if custom_drive_name:
        drive_name = custom_drive_name
    unique_check = params.get("unique_check", False)

    def cleanup():
        try:
            logger.info(f"Удаление диск '{drive_name}'...")
            my_files_page.find_click_header_menu("Документы")
            my_files_page.find_click_side_menu("Общие диски")
            if my_files_page.find_file_by_name(drive_name):
                my_files_page.right_click_and_select_action(drive_name, "Переместить в Корзину")
                my_files_page.popup_action(True)
                logger.info(f"Диск '{drive_name}' удален.")
            else:
                logger.warning(f"Диск '{drive_name}' не найдена при удалении.")
        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}.")
            error_handler.handle_exception(MinorIssue("Удаление провалилось, но тест пройден"), critical=False)

    request.addfinalizer(cleanup)

    if unique_check:
        # Проверка на уникальность имени диска
        my_files_page.find_click_header_menu("Документы")
        my_files_page.find_click_side_menu("Общие диски")
        # Если диск с таким именем уже существует, то продолжаем работать с существующим
        if  my_files_page.find_file_by_name(drive_name):
            return drive_name, my_files_page, xpath
        else:
            # Если диск не найден, то продолжаем создание нового
            my_files_page.click_header_logo_button()

    logger.info(f"Создание диска '{drive_name}' из теста '{test_name}'")

    my_files_page.click_header_logo_button()
    my_files_page.find_click_side_menu("Общие диски")

    # Создание общего диска
    my_files_page.create_drive(drive_name)

    if not my_files_page.find_file_by_name(drive_name):
        raise AssertionError(f"Диск '{drive_name}' не был создан или найден.")

    return drive_name, my_files_page, xpath

# Метод авторизации для УЗ пользователей и эксперта (вызывается в создании соответствующих дарйверов)
def login_user(request, driver, logger, username, password):
    is_combo_test = request.node.get_closest_marker("combo") is not None
    browser_type = request.node.callspec.params.get("browser_type", "chrome")

    if is_combo_test:
        driver_instance = BrowserDriver(browser_type=browser_type)
        driver = driver_instance.initialize_driver()
        error_handler = ErrorHandler(driver, logger)
        login_page = LoginPage(driver, logger)

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()
        assert login_page.check_account_button(), "Авторизация не удалась."
        error_handler.clear_browser_logs()

        yield driver
        driver_instance.cleanup()

    else:
        error_handler = ErrorHandler(driver, logger)
        login_page = LoginPage(driver, logger)

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()
        assert login_page.check_account_button(), "Авторизация не удалась."
        error_handler.clear_browser_logs()

        yield driver

# Хук для настройки окружения перед запуском тестов
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Формирует Licence_Properties. Добавляет сведения о браузере, url и лицензиях в отчет allure"""
    """Запускаем хук только если pytest вызван с `tests/check_url`."""
    command_line_args = sys.argv  # Получаем аргументы запуска pytest

    #Уникальная временная метка начала теста
    if not hasattr(config, 'workerinput'):  # Проверяем, не является ли это воркером xdist
        config._log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Проверяем, что команда - содержит аргумент `tests/check_url` и формируем или ищем файл лицензий
    if "prepare" in getattr(config.option, "markexpr", ""):
        print("Запускаем проверку лицензий")
        if not hasattr(config, 'workerinput'):  # Проверяем, не является ли это воркером xdist
            os.makedirs("log", exist_ok=True)
            os.makedirs("log/screenshots", exist_ok=True)
            os.makedirs("allure_results", exist_ok=True)
            os.makedirs("allure_reports", exist_ok=True)
            os.makedirs("resources/downloads", exist_ok=True)
            os.makedirs("resources/uploads", exist_ok=True)

            raw = config.getoption("browser")
            browsers = [b.strip().lower() for b in raw.split(",")]
            if "all" in browsers:
                browser_list = ["chrome", "firefox", "edge"]
            else:
                browser_list = list(dict.fromkeys(browsers))  # Убираем дубликаты, сохраняем порядок
            browser_type = browser_list[0]  # Первый браузер для инициализации
            driver_instance = BrowserDriver(browser_type=browser_type)

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
                file.write(f"Browser={','.join(browser_list)}\n")

                # Записываем только отличающиеся параметры
                for key, value in diff_licence.items():
                    file.write(f"{key}={value}\n")

                # В конце добавляем путь к файлу с полным списком лицензий
                # file.write(f"Licence.Properties={LICENCE_OUTPUT_FILE}\n")
        if hasattr(config, 'workerinput'):
            # logger.info("Запуск на воркере — загрузка не производится.")
            return
    else:
         licence_file = os.path.join("log", "licence_properties.json")  # Путь к файлу лицензий
         if not os.path.exists(licence_file):
             pytest.exit("Файл licence_properties.json отсутствует! Запустите `pytest -m prepare` для его формирования.")
         else:
            print("Пропускаем проверку лицензий, лицензии сформированы")

# Код действий в конце всех тестов
def pytest_unconfigure(config):
    if hasattr(config, 'workerinput'):
        return  # Это воркер — выходим сразу

    args = config.invocation_params.args
    timestamp = getattr(config, "_log_timestamp", "unknown_time")

    # Извлекаем маркер из -m
    marker_name = None
    if "-m" in args:
        try:
            index = args.index("-m")
            marker_name = args[index + 1].strip('"\'')
        except IndexError:
            pass

    # Если маркер не указан — берём имя первого тестового файла
    if not marker_name:
        test_files = [arg for arg in args if arg.endswith(".py")]
        if test_files:
            marker_name = os.path.splitext(os.path.basename(test_files[0]))[0]
        else:
            marker_name = "no_marker"

    # Очистка URL и маркера — компактно и прямо тут
    url_clean = re.sub(r"_+", "_", re.sub(r"[^\w]", "_", re.sub(r"^https?://", "", URL or "no_url"))).strip("_")
    marker_clean = re.sub(r"_+", "_", re.sub(r"[^\w]", "_", marker_name or "no_marker")).strip("_")

    # Финальное имя лога
    merged_log_name = f"log/{marker_clean}_{url_clean}_{timestamp}.log"

    # Склейка логов
    log_files = glob.glob("log/project_*.log")
    if log_files:
        with open(merged_log_name, "w", encoding="utf-8") as merged:
            for f in log_files:
                with open(f, "r", encoding="utf-8") as part:
                    merged.write(part.read())
        for f in log_files:
            os.remove(f)
        print(f"[xdist] Логи из {len(log_files)} файлов объединены в {merged_log_name}")
    else:
        print("[xdist] Не найдено логов для склейки")

    if os.path.exists(PROFILES_PATH):
        for item in os.listdir(PROFILES_PATH):
            item_path = os.path.join(PROFILES_PATH, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    os.remove(item_path)
            except Exception as e:
                print(f"[CLEANUP] Не удалось удалить {item_path}: {e}")
        print(f"[CLEANUP] Все профили в '{PROFILES_PATH}' удалены.")
    else:
        print(f"[CLEANUP] Папка '{PROFILES_PATH}' не найдена.")