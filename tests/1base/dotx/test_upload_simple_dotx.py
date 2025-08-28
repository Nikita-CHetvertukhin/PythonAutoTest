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
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx"
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_upload_simple_dotx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет загрузку Dotx"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    logger.info("Начало проверки загруженного шаблона")
    # Открытие загруженного файла
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    my_files_editor_page.waiting_status_after("open")