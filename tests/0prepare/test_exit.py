import pytest
from pages.base_page import BasePage
from locators.base_locators import BaseLocators
from pages.login_page import LoginPage
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.prepare
def test_exit(error_handler, logger, admin_driver):
    """Тест проверяет корректность выхода из УЗ."""
    base_page = BasePage(admin_driver, logger)
    login_page = LoginPage(admin_driver, logger)
    
    logger.info("Начало проверки успешного выхода из УЗ")
    base_page.exit_from_account()
    
    # Обновляем страницу и ждём загрузки
    refresh_and_wait(admin_driver, logger)

    assert not login_page.check_account_button(), "Элемент личного кабинета найден после выхода из УЗ."
    logger.info("Тест выхода из УЗ и прерывания сессии успешно пройден")