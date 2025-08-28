import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from utils.refresh_and_wait import refresh_and_wait
from utils.licence_checker import is_licence_enabled
from settings.variables import SHARE_DRIVES
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.skipif(
    not is_licence_enabled(SHARE_DRIVES),
    reason=f"Лицензия '{SHARE_DRIVES}' отключена — тест пропущен"
)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_drive(error_handler, logger, admin_driver, setup_create_delete_drive):
    """Тест проверяет создание общего диска"""
    drive_name, my_files_page, xpath = setup_create_delete_drive

    logger.info("Начало проверки создания общего диска")
    # Открытие созданной папки
    my_files_page.right_click_and_select_action(drive_name, "Открыть")
    time.sleep(1) # ToDo пока не знаю, что смотерть когда октрываю пустую папку
    # Обновление страницы
    refresh_and_wait(admin_driver, logger)
    # Финальная проверка присутствия файла в системе и корректного формата
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Общие диски")
    my_files_page.find_file_by_name(drive_name, "folder")