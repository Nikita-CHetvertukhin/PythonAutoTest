import pytest
from utils.exception_handler.decorator_error_handler import exception_handler

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_opening_task_context(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет Открытие задачи через ПКМ - Открыть"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки открытия задачи через ПКМ - Открыть")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
