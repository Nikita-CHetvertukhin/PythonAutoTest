import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import ADMIN_LOGIN
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx",
    "publishing_from": [f"{ADMIN_LOGIN}"]
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_unpublish_dotx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет снятие с публикации простого Dotx"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    logger.info("Начало проверки снятия с публикации простого dotx")
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Шаблоны")
    my_files_page.right_click_and_select_action(file_name, "Снять с публикации")

    refresh_and_wait(admin_driver, logger)

    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Шаблоны")
    assert my_files_page.find_file_by_name(file_name) is None, f"Шаблон {file_name} успешно снят с публшикации"