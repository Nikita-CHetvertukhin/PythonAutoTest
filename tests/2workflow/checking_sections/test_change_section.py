import pytest
import allure
from pages.my_files_page import MyFilesPage
from locators.base_locators import BaseLocators
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@exception_handler
def test_change_section(request, error_handler, logger, admin_driver):
    """Проверка доступности вкладок и корректности отображения колонок в разделе 'Мои файлы'."""
    logger.info(f"Начало проверки")

    my_files_page = MyFilesPage(admin_driver, logger)

    # Маппинг: раздел → соответствующая вкладка
    section_map = {
        "Мои задачи": "Мои задачи",
        "Документы": "Мои файлы"
    }

    # Дополнительные вкладки для проверки
    extra_tabs = ["Недавние", "Доступные мне"]

    for i in range(5):
        for header, side in section_map.items():
            my_files_page.find_click_header_menu(header)
            my_files_page.find_click_side_menu(side)
            my_files_page.check_error()

    for i in range(5):
        for tab in extra_tabs:
            my_files_page.find_click_side_menu(tab)
            my_files_page.check_error()