import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators
from utils.download_manager import DownloadManager

@pytest.mark.parametrize(
    "setup_create_delete_file",[{
    "file_type": "Новый документ"
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_file_from_task(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет функционал удаления прикрепленного документа в задаче"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_tasks_page = MyTasksPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки функционала удаления прикрепленного докмуента в задаче")
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.create_task(task_name=f'task_{file_name}', task_type="Простая задача", executor=ADMIN_LOGIN, attache_file=file_name)
    
    goal_task = my_tasks_page.find_task_by_name(f'task_{file_name}')
    goal_task.click()
    time.sleep(1)  # Заменить на динамическое ожидание пояаления задачи
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DELETE_FILE_BUTTON, timeout=3).click()
    time.sleep(1)
    assert not my_tasks_page.find_document_in_task(file_name), f"Ошибка: файл '{file_name}' найден после удаления!"
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DELETE_BUTTON, timeout=3).click()
    logger.info("Тест выполнен. Задача успешно удалена через кнопку 'Удалить' в taskform")