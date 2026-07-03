import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
from utils.download_manager import DownloadManager
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_String.dotx",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
@allure.epic('Коробка')
@allure.feature('Формулы')
@allure.title('Проверка текстовых формул')
def test_text_formuls(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет работу текстовых формул"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки работы текстовых формул")
    my_files_editor_page.open_side_panel_in_doc("Анкета")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Текст", "ID1", "Godzilla")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Текст", "ID2", "Doc")
    xpath.find_clickable(MyFilesEditorLocators.SAVE_BUTTON).click()
    # Проверки работы формул
    assert my_files_editor_page.check_content_in_doc("Godzilla")
    assert my_files_editor_page.check_content_in_doc("Doc")
    assert my_files_editor_page.check_content_in_doc("Условие: переменная не пустая ID1 != \"\"")
    assert my_files_editor_page.check_content_in_doc("Условие: переменная не пустая ! (ID1 == \"\")")
    assert not my_files_editor_page.check_content_in_doc("Условие: переменная пустая ID1 == \"\"")
    assert not my_files_editor_page.check_content_in_doc("Условие: переменная пустая ID1 == null")
    assert my_files_editor_page.check_content_in_doc("zilla")
    assert my_files_editor_page.check_content_in_doc("Doczilla - лучший продукт!")
    assert my_files_editor_page.check_content_in_doc("8")