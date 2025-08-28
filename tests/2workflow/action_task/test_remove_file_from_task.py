import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators
from utils.download_manager import DownloadManager
import allure
from utils.get_date import get_timestamp, get_uuid

file_name = f"{get_uuid()}_remove_file_from_task_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "file_type": "Новый документ",
            "file_name": file_name,
            "unique_check": True
        },
        {
            "task_type" : "Простая задача",
            "task_executor": ADMIN_LOGIN,
            "attache_file": file_name
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_file_from_task(error_handler, logger, admin_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет функционал удаления прикрепленного документа в задаче"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки функционала удаления прикрепленного докмуента в задаче")
    
    goal_task = my_tasks_page.find_file_by_name(task_name)
    goal_task.click()
    time.sleep(1)  # Заменить на динамическое ожидание появления задачи
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DELETE_FILE_BUTTON, timeout=3).click()
    time.sleep(1)
    assert not my_tasks_page.find_document_in_task(file_name), f"Ошибка: файл '{file_name}' найден после удаления!"