import pytest
from utils.exception_handler.decorator_error_handler import exception_handler

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_8_2_deleting_task(error_handler, logger, admin_driver, setup_create_task):
    """Тест проверяет Удаление задачи через ПКМ - Удалить"""
    task_name, my_tasks_page, xpath = setup_create_task

    logger.info("Начало проверки удаления задачи через ПКМ - Удалить")
    my_tasks_page.right_click_and_select_action(task_name, "Удалить")
    my_tasks_page.find_click_side_menu("Удаленные")
    assert my_tasks_page.find_task_by_name(task_name) is not None, f"Задача '{task_name}' не найдена в разделе 'Удаленные'"