import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators
from pages.my_files_editor_page import MyFilesEditorPage
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
            "task_type" : "Простой процесс",
            "deadline": get_date("today"),
            "task_executor": ADMIN_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_approval_task_from_my_files(error_handler, logger, admin_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет создание задачи через 'Документ'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    my_files_editor_page.wf_action_in_file(action_name="Выполнить")
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    assert not my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не исчезла после выполнения."
    my_tasks_page.find_click_side_menu("Закрытые")
    assert my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не найдена в разделе 'Закрытые'"