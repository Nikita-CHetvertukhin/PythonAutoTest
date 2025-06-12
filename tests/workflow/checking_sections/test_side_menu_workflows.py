import pytest
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from pages.workflows_page import WorkflowsPage
from locators.workflows_locators import WorkflowsLocators

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор, обрабатывающий исключения, чтобы тест не прерывался неожиданно
def test_side_menu_workflows(error_handler, logger, admin_driver):
    """Тест проверяет доступность вкладок в разделе 'Рабочие процессы' и фиксирует ошибки, если они есть."""

    logger.info("Начало проверки доступности разделов и вкладок 'Рабочие процессы'")
    workflows_page = WorkflowsPage(admin_driver, logger)

    tabs = ["Корзина", "Шаблоны процессов"]
    columns_to_check = ["check", "Название", "Дата изменения", "Автор"]
    failed_tabs = []

    workflows_page.find_click_header_menu("Рабочие процессы")

    for tab_name in tabs:
        workflows_page.find_click_side_menu(tab_name)

        success, details = workflows_page.checking_success_side_menu(
            tab_name, WorkflowsLocators.WORKFLOWS_TITLE, WorkflowsLocators.WORKFLOWS_COLUMNS, columns_to_check, None
        )

        if success:
            logger.info(f"Раздел '{tab_name}' загружен успешно.")
        else:
            error_handler.handle_exception(MinorIssue(f"Ошибка в разделе '{tab_name}' Детали: {details}"))
            logger.warning(f"Ошибка в разделе '{tab_name}': {details}")
            failed_tabs.append({"tab": tab_name, "details": details})

    if failed_tabs:
        error_messages = "\n".join([f"Раздел '{entry['tab']}': {entry['details']}" for entry in failed_tabs])
        logger.error(f"Тест провален. Ошибки:\n{error_messages}")
        pytest.fail(f"Тест провален. Ошибки:\n{error_messages}", pytrace=False)
    else:
        logger.info("Все проверки вкладок 'Рабочие процессы' прошли успешно.")