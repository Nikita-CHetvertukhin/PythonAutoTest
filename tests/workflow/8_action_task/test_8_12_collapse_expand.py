import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_8_12_collapse_expand(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет сворачивание/разворачивание taskform несколкьо раз"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки сворачивания/разворачивания taskfowm")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    for i in range(5):
        logger.info(f"Итерация {i + 1}: разворачивание taskform")
        xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_EXPAND_BUTTON, timeout=3).click()
        logger.info(f"Итерация {i + 1}: сворачивание taskform")
        xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_COLLAPSE_BUTTON, timeout=3).click()
        assert xpath.find_visible(MyTasksLocators.MY_TASKS_TITLE, timeout=3) is not None, \
            f"Ошибка: Заголовок задачи не виден после сворачивания taskform (итерация {i + 1})"