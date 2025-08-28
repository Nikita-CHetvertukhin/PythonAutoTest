import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новый документ",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_docx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет создание простого Docx"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    logger.info("Начало проверки создания простого docx")
    # Возврат в корень "Мои файлы"
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    # Обновление страницы
    refresh_and_wait(admin_driver, logger)
    # Финальная проверка присутствия файла в системе и корректного формата
    my_files_page.find_file_by_name(file_name, "docx")