#Глобальный импорт
import pytest
#Локальный импорт
from utils.browser_driver import BrowserDriver
from settings.variables import Browser
from utils.exception_handler.configure_logging import configure_logging
from utils.exception_handler.error_handler import ErrorHandler
from pages.login_page import LoginPage
from settings.variables import Admin_Login, Admin_Password
from utils.exception_handler.decorator_error_handler import MinorIssue

@pytest.fixture(scope="function")
def driver():
    """Создание нового драйвера для каждого теста"""
    driver_instance = BrowserDriver(browser_type=Browser)
    driver = driver_instance.initialize_driver()

    yield driver  # Передаём драйвер в тесты

    driver.quit()  # Закрываем браузер после теста

@pytest.fixture(scope="session")
def logger():
    """
    Фикстура для логгера, который будет использоваться в тестах.
    """
    return configure_logging()

@pytest.fixture(scope="function")
def error_handler(driver, logger):
    """
    Фикстура для инициализации ErrorHandler с использованием driver и logger.
    """
    return ErrorHandler(driver, logger)

@pytest.fixture(scope="function")
def admin_driver(driver, logger, error_handler):
    """Создаёт новый браузер и выполняет авторизацию"""
    login_page = LoginPage(driver, logger)

    login_page.enter_username(Admin_Login)
    login_page.enter_password(Admin_Password)
    login_page.click_login()

    assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."

    return driver  # Передаём браузер без закрытия (его закроет driver)