import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новую папку",
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_folder(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет удаление папки"""
    file_name, my_files_page, xpath = setup_create_delete_file

    logger.info("Начало проверки удаления папки")
    # Перемещение в корзину
    my_files_page.right_click_and_select_action(file_name, "Переместить в Корзину")
    
    # Пауза для стабильности
    time.sleep(1)

    # Переключение на корзину и проверка наличия папки
    my_files_page.find_click_side_menu("Корзина")
    my_files_page.find_file_by_name(file_name, "folder")