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
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новую папку",
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_drive_by_folder(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет создание общего диска из папки"""
    file_name, my_files_page, xpath = setup_create_delete_file

    logger.info("Начало проверки создания общего диска из папки")
    # Открытие созданной папки
    my_files_page.right_click_and_select_action(file_name, "Сделать общим диском")
    # Возврат в корень "Мои файлы"
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Общие диски")
    my_files_page.find_file_by_name(file_name, "folder")
    # Обновление страницы
    refresh_and_wait(admin_driver, logger)
    # Финальная проверка присутствия файла в системе и корректного формата
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Общие диски")
    my_files_page.find_file_by_name(file_name, "folder")
    my_files_page.right_click_and_select_action(file_name, "Переместить в Корзину")
    my_files_page.popup_action(True)