import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
import allure
from settings.variables import ADMIN_LOGIN
from utils.get_date import get_timestamp, get_uuid

process_name = f"{get_uuid()}_deleting_custom_task_{get_timestamp()}"

@allure.severity(allure.severity_level.NORMAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_process", "setup_create_delete_task"),
    [(
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Usual_Process.dzwf",
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
def test_deleting_custom_task(error_handler, logger, admin_driver, setup_create_delete_process, setup_create_delete_task):
    """Тест проверяет Удаление кастомной (корневой + вложенных) задачи через ПКМ - Удалить"""
    process_name, workflows_page, xpath = setup_create_delete_process
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки удаления задачи через ПКМ - Удалить")
    my_tasks_page.right_click_and_select_action(task_name, "Удалить")
    my_tasks_page.find_click_side_menu("Удаленные")
    assert my_tasks_page.find_file_by_name(task_name) is not None, f"Задача '{task_name}' не найдена в разделе 'Удаленные'"