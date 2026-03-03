import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_header_buttons(error_handler, logger, admin_driver):
    """Тест проверяет открытие вкладок в разделе 'Настройки'"""
    my_files_page = MyFilesPage(admin_driver, logger)

    logger.info("Начало проверки вкладок в разделе 'Настройки'")
    my_files_page.find_click_header_menu("Настройки", "Параметры")
    my_files_page.check_error(should_find_error=False)
    my_files_page.find_click_header_menu("Настройки", "Хранилище паролей")
    my_files_page.check_error(should_find_error=False)
    logger.info("Вкладки в разделе 'Настройки' открыты корректно")