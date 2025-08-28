import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from utils.refresh_and_wait import refresh_and_wait
from utils.download_manager import DownloadManager
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_download_simple_dotx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет скачивание простого Dotx"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки скачивания шаблона")
    # Скачивание и проверка
    my_files_editor_page.click_file_and_click("Скачать")
    assert download_manager.verify_downloaded_file(f"{file_name}.dotx"), f"Ошибка: файл '{file_name}.dotx' не был загружен!"
    logger.info(f"{file_name}.dotx успешно скачен")