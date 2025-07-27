import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators
from utils.download_manager import DownloadManager
import allure
from utils.get_date import get_timestamp

file_name = f"AQA_test_download_file_from_task_{get_timestamp()}"

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
def test_download_file_from_task(error_handler, logger, admin_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет функционал прикрепления документа к задаче"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_tasks_page = MyTasksPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки функционала прикрепления докмуента к задаче")
    goal_task = my_tasks_page.find_file_by_name(task_name)
    goal_task.click()
    time.sleep(1)  # Заменить на динамическое ожидание появления задачи
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DOWNLOAD_FILE_BUTTON, timeout=3).click()
    assert download_manager.verify_downloaded_file(f"{file_name}.docx"), f"Ошибка: файл '{file_name}.docx' не был загружен!"