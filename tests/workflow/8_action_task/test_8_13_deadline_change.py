import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from utils.refresh_and_wait import refresh_and_wait
import time
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.parametrize(
    "setup_create_delete_task",
    [{"deadline": get_date("today")}],
    indirect=True
)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот

def test_8_13_deadline_change(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет изменение дедлайна для задачи"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки изменения дедлайна")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    my_tasks_page.task_deadline_properties(deadline=get_date("tomorrow"), action="set")
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
    refresh_and_wait(admin_driver, logger)

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1)  # TODO: заменить на ожидание состояния страницы
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_deadline_properties(deadline=get_date("tomorrow"), action="check"), "Дедлайн не совпадает."