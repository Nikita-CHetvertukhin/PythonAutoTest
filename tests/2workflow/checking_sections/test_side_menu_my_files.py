import pytest
import allure
from pages.my_files_page import MyFilesPage
from locators.base_locators import BaseLocators
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize("tabs, columns", [
    (["Доступные мне", "Недавние", "Корзина"], ["check", "Название", "Дата изменения", "Автор", "Комментарий"]),
    (["Мои файлы"], ["check", "Название", "Дата изменения", "Автор", "Стадия", "Комментарий"]),
    (["Шаблоны"], ["check", "Название", "Версия", "Автор", "Комментарий"]),
])
@exception_handler
def test_side_menu_my_files(request, error_handler, logger, admin_driver, tabs, columns):
    """Проверка доступности вкладок и корректности отображения колонок в разделе 'Мои файлы'."""
    logger.info(f"Начало проверки вкладок: {tabs}")

    page = MyFilesPage(admin_driver, logger)
    page.find_click_header_menu("Документы")

    failed_tabs = []

    for tab_name in tabs:
        page.find_click_side_menu(tab_name)

        success, details = page.checking_success_side_menu(
            tab_name, BaseLocators.BODY_TITLE, BaseLocators.BODY_COLUMNS, columns
        )

        if success:
            logger.info(f"Раздел '{tab_name}' загружен успешно.")
        else:
            error_handler.handle_exception(MinorIssue(f"Ошибка в разделе '{tab_name}' Детали: {details}"), critical=False)
            logger.warning(f"Ошибка в разделе '{tab_name}': {details}")
            failed_tabs.append({"tab": tab_name, "details": details})

    if failed_tabs:
        error_messages = "\n".join([f"Раздел '{entry['tab']}': {entry['details']}" for entry in failed_tabs])
        logger.error(f"Тест провален. Ошибки:\n{error_messages}")
        pytest.fail(f"Тест провален. Ошибки:\n{error_messages}", pytrace=False)
    else:
        logger.info("Все проверки вкладок прошли успешно.")