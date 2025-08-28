import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize("setup_create_delete_task",[{
    "deadline": get_date("today"),
    "task_type": "Простой процесс",
    "task_executor": ADMIN_LOGIN
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_approval_task_from_my_tasks(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет выполнение задачи из меню 'Мои задачи'"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Проверка выполнения задачи из меню 'Мои задачи'")
    subtasks = [(1, "Задача", "Выполнить")]
    my_tasks_page.complete_task(task_name, subtasks)

    assert not my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не исчезла после выполнения."
    my_tasks_page.find_click_side_menu("Закрытые")
    assert my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не найдена в разделе 'Закрытые'"