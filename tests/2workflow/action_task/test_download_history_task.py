import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from locators.my_tasks_locators import MyTasksLocators
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_download_history_task(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет возможность скачивания истории задачи в различных форматах"""
    formats = ["pdf", "xlsx", "doc"]
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки возможности скачивания истории задачи")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_SHOW_SYSTEM_EVENTS_BUTTON, timeout=3).click()
    for fmt in formats:
        my_tasks_page.download_history_task(task_name, fmt)
    logger.info("Проверка скачивания истории задачи завершена успешно")