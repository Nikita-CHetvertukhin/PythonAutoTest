import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
@allure.epic('Коробка')
@allure.feature('Разделы')
@allure.title('Проверка базовых вкладок в хедере')
def test_header_buttons(error_handler, logger, admin_driver):
    """Тест проверяет открытие базовых вкладок в хедере"""
    my_files_page = MyFilesPage(admin_driver, logger)

    logger.info("Начало проверки базовых разделов хедера")
    my_files_page.find_click_header_menu("Статистика", "Статистика по файлам")
    my_files_page.check_error(should_find_error=False)
    my_files_page.find_click_header_menu("Статистика", "Статистика по пользователям")
    my_files_page.check_error(should_find_error=False)
    my_files_page.find_click_header_menu("Статистика", "Статистика по времени")
    my_files_page.check_error(should_find_error=False)
    my_files_page.find_click_header_menu("Справочники")
    my_files_page.check_error(should_find_error=False)
    my_files_page.find_click_header_menu("Документы")
    my_files_page.check_error(should_find_error=False)
    logger.info("Базовые разделы хедера открыты успешно")