import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import ADMIN_LOGIN
import allure
from utils.get_date import get_timestamp, get_uuid

process_name = f"{get_uuid()}_test_automat_create_subtask_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_process", "setup_create_delete_task"),
    [(
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Automatizations_Create_subtask.dzwf",
            "publishing": True,
            "unique_check": True
        },
        {
            "task_type" : process_name,
            "task_executor": ADMIN_LOGIN
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automat_create_subtask(error_handler, logger, admin_driver, setup_create_delete_process, setup_create_delete_task):
    """Тест проверяет работу автоматизации по созданию подзадачи"""
    process_name, workflows_page, xpath = setup_create_delete_process
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Начало проверки автоматизации по созданию подзадачи")
    subtasks = [(2, "Созданная подзадача", "Выполнить"),(1, "Основная задача", "Выход")]
    my_tasks_page.complete_task(task_name, subtasks)

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    assert not my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не исчезла после выполнения."