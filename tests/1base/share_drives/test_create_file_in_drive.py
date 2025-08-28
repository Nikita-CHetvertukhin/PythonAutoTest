import pytest
import time
from pages import my_files_editor_page
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from utils.refresh_and_wait import refresh_and_wait
from utils.licence_checker import is_licence_enabled
from settings.variables import SHARE_DRIVES
from utils.get_date import get_timestamp, get_uuid
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.skipif(
    not is_licence_enabled(SHARE_DRIVES),
    reason=f"Лицензия '{SHARE_DRIVES}' отключена — тест пропущен"
)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_file_in_drive(error_handler, logger, admin_driver, setup_create_delete_drive):
    """Тест проверяет создание файлов на общем диске"""
    drive_name, my_files_page, xpath = setup_create_delete_drive
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    file_name = f"{get_uuid()}_docx_test_create_file_in_drive{get_timestamp()}"

    logger.info("Начало проверки создания файлов в общем диске")
    # Открытие созданного диска
    my_files_page.right_click_and_select_action(drive_name, "Открыть")
    time.sleep(1) # ToDo пока не знаю, что смотерть когда октрываю пустую папку
    # Создание и проверка файла
    my_files_page.create_file(file_name, "Новый документ")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    my_files_editor_page.waiting_status_after("open")