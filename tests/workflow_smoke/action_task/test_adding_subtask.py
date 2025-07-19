import pytest
from utils.exception_handler.decorator_error_handler import exception_handler

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_adding_subtask(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет создание подзадачи"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки создания подзадачи")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
    my_tasks_page.create_subtask(subtask_name=f"{task_name}_subtask")
    assert my_tasks_page.find_task_by_name(f"{task_name}_subtask") is not None, f"Ошибка: Подзадача '{task_name}_subtask' не найдена после создания."