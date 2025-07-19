import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_ID1.docz",
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automat_name(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет автоматическую подстановку значения перемнной из анкеты в название задачи"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_tasks_page = MyTasksPage(admin_driver, logger)
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    logger.info("Начало проверки автоматической подстановки значения переменной в название задачи")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Текст", "AQA_ID1", file_name)
    xpath.find_clickable(MyFilesEditorLocators.SAVE_BUTTON).click()
    my_tasks_page.create_task(task_name="${ID1}", task_type="Простая задача", from_file=True)
    time.sleep(1)
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    assert my_tasks_page.find_task_by_name(file_name), f"Ошибка: Задача с именем '{file_name}' не найдена в списке задач."
    my_tasks_page.right_click_and_select_action(file_name, "Удалить")