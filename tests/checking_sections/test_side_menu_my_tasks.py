import pytest
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators

@exception_handler  # Декоратор, обрабатывающий исключения, чтобы тест не прерывался неожиданно
def test_side_menu_my_tasks(error_handler, logger, admin_driver):
    """Тест проверяет доступность вкладок в разделе 'Мои задачи' и фиксирует ошибки, если они есть."""

    logger.info("Начало проверки доступности разделов 'Мои задачи'")
    my_tasks_page = MyTasksPage(admin_driver, logger)

    tabs = ["Отслеживаемые", "Просроченные", "Закрытые", "Все задачи", "Удаленные","Мои задачи"]
    columns_to_check = ["check", "Задача", "Статус", "Исполнитель", "Автор", "Дедлайн", "Дата изменения"]
    failed_tabs = []

    my_tasks_page.find_click_header_menu("Мои задачи")

    for tab_name in tabs:
        my_tasks_page.find_click_side_menu(tab_name)

        success, details = my_tasks_page.checking_success_side_menu(
            tab_name, MyTasksLocators.MY_TASKS_TITLE, MyTasksLocators.MY_TASKS_COLUMNS, columns_to_check, None
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
        logger.info("Все проверки вкладок 'Мои задачи' прошли успешно.")