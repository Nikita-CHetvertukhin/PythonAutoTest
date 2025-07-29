import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from locators.my_files_editor_locators import MyFilesEditorLocators
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, USER1_LOGIN
import allure
from utils.get_date import get_timestamp, get_uuid

process_name = f"{get_uuid()}_test_check_observer_manual_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.combo
@pytest.mark.parametrize(("setup_create_delete_process","setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Observer_Reader_Manual.dzwf",
            "publishing": True,
            "unique_check": True
        },
        {
            "file_type": "Новый документ",
            "open_file": True
        },
        {
            "task_type" : process_name,
            "task_executor": ADMIN_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_check_observer_manual(request, error_handler, logger, admin_driver, user1_driver, setup_create_delete_process, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет назначение наблюдателя и его уровни доступа"""
    process_name, workflows_page, xpath = setup_create_delete_process
    file_name, my_files_page, xpath  = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    user1_my_tasks_page = MyTasksPage(user1_driver, logger)
    logger.info("Начало проверки назначения наблюдателя и его уровней доступа")
    # Добавляем наблюдателя
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.open_subtask(task_name, subtask_massive=[(1, "Задача")])
    my_tasks_page.task_oberver_properties(USER1_LOGIN)
    # Проверяем доступ к докмуенту для наблюдателя
    my_tasks_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    time.sleep(2)  # TODO заменить на динамическое ожидание при октрытии файла
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    logins_and_access = [(USER1_LOGIN, "Просмотр")]
    assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access}."
    
    # Проверяем доступ к полям задачи для наблюдателя
    user1_my_tasks_page.find_click_header_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Отслеживаемые")
    time.sleep(3) # TODO Разобраться что блокирует открытие подзадачи без ожидания. Мне кажется даже при выключенных уведомлениях появляется какой-то фрейм на всю страницу не видимый для юзера, который сбивает селениум
    user1_my_tasks_page.open_subtask(task_name, subtask_massive=[(1, "Задача")])
    assert user1_my_tasks_page.check_access_to_task_fields(fields_massive=[]), "Ошибка в доступе к полям задачи для наблюдателя."
