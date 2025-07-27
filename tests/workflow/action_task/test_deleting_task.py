import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
import allure

@allure.severity(allure.severity_level.NORMAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize("setup_create_delete_task", [{
        "skip_cleanup": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_deleting_task(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет Удаление задачи через ПКМ - Удалить"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки удаления задачи через ПКМ - Удалить")
    my_tasks_page.right_click_and_select_action(task_name, "Удалить")
    my_tasks_page.find_click_side_menu("Удаленные")
    assert my_tasks_page.find_file_by_name(task_name) is not None, f"Задача '{task_name}' не найдена в разделе 'Удаленные'"