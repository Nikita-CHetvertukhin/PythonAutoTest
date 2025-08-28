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
    "upload_file_name": "AQA_ID1.docz",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_download_questionnary_docx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет скачивание Анкеты в docx формате"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки скачивания Анкеты в docx формате")
    # Открытие созданного файла
    my_files_editor_page.find_and_send_variable_in_questionnaire("Текст", "AQA_ID1", file_name)
    xpath.find_clickable(MyFilesEditorLocators.SAVE_BUTTON).click()
    my_files_editor_page.finish_questionnaire("Скачать DOCX")
    assert download_manager.verify_downloaded_file(f"{file_name}.docx"), f"Ошибка: файл '{file_name}.docx' не был загружен!"
    logger.info(f"{file_name}.docx успешно скачен")