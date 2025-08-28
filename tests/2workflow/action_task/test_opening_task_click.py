import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_opening_task_click(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет Открытие задачи через клик ЛКМ"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки открытия задачи клик ЛКМ")
    goal_task = my_tasks_page.find_file_by_name(task_name)
    goal_task.click()
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
