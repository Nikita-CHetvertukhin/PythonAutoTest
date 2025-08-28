import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from settings.variables import AQA_GROUP
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.combo
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx",
    "publishing_from": [f"{AQA_GROUP}"]
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_publish_to_group(error_handler, logger, admin_driver, user1_driver, setup_create_delete_file):
    """Тест проверяет публикацию простого Dotx на группу"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    user1_files_pages = MyFilesPage(user1_driver, logger)

    logger.info("Начало проверки публикации простого Dotx на группу")
    user1_files_pages.click_header_logo_button()
    user1_files_pages.find_click_header_menu("Документы")
    user1_files_pages.find_click_side_menu("Шаблоны")
    assert user1_files_pages.find_file_by_name(file_name) is not None, f"Шаблон {file_name} не найден в списке опубликованных"
    logger.info(f"{file_name}.dotx успешно опубликован")