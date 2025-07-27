import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from locators.my_tasks_locators import MyTasksLocators
from selenium.webdriver.common.keys import Keys
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_closing_taskform(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяетзакрытие taskfowm через нажатие ESC или через клик по 'Закрыть'"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки закрытия taskfowm через нажатие ESC")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
    xpath.find_visible(MyTasksLocators.MY_TASKS_TASKFORM).send_keys(Keys.ESCAPE)
    assert xpath.wait_until_elements_not_present(MyTasksLocators.MY_TASKS_TASKFORM, timeout=3), "Ошибка: taskform не закрылся после клика по заголовку (Вне области taskform)."

    logger.info("Начало проверки закрытия taskfowm через клик по 'Закрыть'")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
    assert xpath.wait_until_elements_not_present(MyTasksLocators.MY_TASKS_TASKFORM, timeout=3), "Ошибка: taskform не закрылся после клика по заголовку (Вне области taskform)."