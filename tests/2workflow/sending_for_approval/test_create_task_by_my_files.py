import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "file_type": "Новый документ",
            "open_file": True
        },
        {
            "task_type" : "Простая задача",
            "description": "test_description",
            "deadline": get_date("today"),
            "task_executor": ADMIN_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_task_by_my_files(error_handler, logger, admin_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет создание задачи через 'Документ'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Проверка созданной задачи через 'Мои задачи'")
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    goal_task = my_tasks_page.find_file_by_name(task_name)
    goal_task.click()
    time.sleep(1)  # Заменить на динамическое ожидание появления задачи
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
    assert my_tasks_page.task_description_properties("test_description", action="check"), "Ошибка: Описание задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_deadline_properties(get_date("today"), action="check"), "Ошибка: Дедлайн задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_executor_properties(ADMIN_LOGIN, action="check"), f"Ошибка: Исполнитель задачи не совпадает с ожидаемым '{ADMIN_LOGIN}'."