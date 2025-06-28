import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import USER1_LOGIN
from utils.refresh_and_wait import refresh_and_wait
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_8_15_change_executor_subtask(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет создание подзадачи"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки создания подзадачи")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    my_tasks_page.create_subtask(subtask_name=f"{task_name}_subtask")
    assert my_tasks_page.find_task_by_name(f"{task_name}_subtask") is not None, f"Ошибка: Подзадача '{task_name}_subtask' не найдена после создания."
    my_tasks_page.right_click_and_select_action(f"{task_name}_subtask", "Открыть")
    my_tasks_page.task_executor_properties(executor_login=USER1_LOGIN, action="set")
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
    
    refresh_and_wait(admin_driver, logger)

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1)  # TODO: заменить на ожидание состояния страницы
    my_tasks_page.right_click_and_select_action(f"{task_name}_subtask", "Открыть")
    assert my_tasks_page.task_executor_properties(executor_login=USER1_LOGIN, action="check"), "Исполнитель подзадачи не совпадает."