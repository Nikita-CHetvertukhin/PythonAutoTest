import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from utils.refresh_and_wait import refresh_and_wait
from utils.get_date import get_timestamp, get_uuid
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новую папку",
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_moved_folder(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет перемещение папки"""
    file_name, my_files_page, xpath = setup_create_delete_file
    test_folder = f"{get_uuid()}_moved_folder_{get_timestamp()}"

    logger.info("Начало проверки перемещения папки")
    # Создание перемещаемой папки
    # refresh_and_wait(admin_driver, logger)
    my_files_page.create_file(test_folder, "Новую папку")
    
    # Перемещение папки
    my_files_page.right_click_and_select_action(test_folder, "Переместить")
    my_files_page.move_to(folder_name=file_name)

    # Проверка, что папка перемещена
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    my_files_page.find_file_by_name(test_folder,"folder")