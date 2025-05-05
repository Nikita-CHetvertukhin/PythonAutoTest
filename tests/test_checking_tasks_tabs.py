import pytest
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
#from locators.tasks_tab_locators import TasksTabLocators
from pages.tasks_tab_page import TasksTabPage

@exception_handler
def test_checking_tasks_tabs(error_handler, logger, admin_driver):
    logger.info("Начало проверки доступности разделов и вкладок Workflow")
    tasks_tab_page = TasksTabPage(admin_driver, logger)

    tasks_tab_page.find_click_header_menu("Мои задачи")

    tasks_tab_page.find_click_side_menu("Отслеживаемые")
    tasks_tab_page.checking_succes("Отслеживаемые")

    tasks_tab_page.find_click_side_menu("Просроченные")
    tasks_tab_page.checking_succes("Просроченные")

    tasks_tab_page.find_click_side_menu("Закрытые")
    tasks_tab_page.checking_succes("Закрытые")

    tasks_tab_page.find_click_side_menu("Все задачи")
    tasks_tab_page.checking_succes("Все задачи")

    tasks_tab_page.find_click_side_menu("Удаленные")
    tasks_tab_page.checking_succes("Удаленные")

    tasks_tab_page.find_click_side_menu("Мои задачи")
    tasks_tab_page.checking_succes("Мои задачи")

    assert True