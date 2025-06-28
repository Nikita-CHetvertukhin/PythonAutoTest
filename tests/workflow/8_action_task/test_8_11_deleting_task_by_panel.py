import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_8_11_deleting_task_by_panel(error_handler, logger, admin_driver, setup_create_task):
    """Тест проверяет удаление задачи через кнопку 'Удалить' в taskform"""
    task_name, my_tasks_page, xpath = setup_create_task

    logger.info("Начало проверки удаления задачи через кнопку 'Удалить' в taskform")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DELETE_BUTTON, timeout=3).click()
    my_tasks_page.find_click_side_menu("Удаленные")
    assert my_tasks_page.find_task_by_name(task_name) is not None, f"Задача '{task_name}' не найдена в разделе 'Удаленные'"