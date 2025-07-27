import pytest  # Импорт библиотеки для работы с тестами
from pages.login_page import LoginPage
from locators.login_locators import LoginLocators
from utils.exception_handler.decorator_error_handler import exception_handler # Декоратор для обработки исключений
from settings.variables import ADMIN_LOGIN, ADMIN_PASSWORD, USER1_LOGIN, USER1_PASSWORD  # Данные для тестирования авторизации
import allure

@allure.severity(allure.severity_level.BLOCKER) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.prepare
@pytest.mark.parametrize("test_suite", [
    # Параметризованные тесты для проверки различных сценариев авторизации
    ("Некорректный логин", ADMIN_LOGIN + "123", ADMIN_PASSWORD, True),  # Ожидаем ошибку из-за неверного логина
    ("Некорректный пароль", ADMIN_LOGIN, ADMIN_PASSWORD + "123", True),  # Ожидаем ошибку из-за неверного пароля
    ("Некорректные логин и пароль", ADMIN_LOGIN + "123", ADMIN_PASSWORD + "123", True),  # Ожидаем ошибку из-за неверного пароля
    ("Успешная авторизация ADMIN", ADMIN_LOGIN, ADMIN_PASSWORD, False)  # Ожидаем успешную авторизацию без ошибок
])
def test_authorization(error_handler, logger, driver, test_suite):
    """Тест авторизации в системе с различными комбинациями логина и пароля."""
    suite_name, login, password, expect_error = test_suite # Распаковываем параметры теста
    login_page = LoginPage(driver, logger)  # Создаём объект страницы логина
    logger.info(f"Начало выполнения теста: {suite_name}")  # Логируем начало теста

    # Вводим данные авторизации и нажимаем "Войти"
    login_page.enter_username(login, log_enabled=True)
    login_page.enter_password(password, log_enabled=True)
    login_page.click_login()

    if expect_error:
        # Проверяем наличие ошибки при авторизации с неверными кредами + отсутствие элемента личного кабинета
        assert login_page.check_error(expect_error, LoginLocators.AUTH_ERROR), "Отсутствие ошибки при попытке входа с неверным логином/паролем"
        assert not login_page.check_account_button(), "Элемент личного кабинета найден. Авторизация выполнена."
        logger.info(f"Тест '{suite_name}' завершён")
    else:
        # Проверяем наличие элемента личного кабинета + отсутствие любых ошибок
        assert login_page.check_error(expect_error), "Присутствует ошибка при успешной авторизации"
        assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
        logger.info(f"Тест '{suite_name}' завершился успешно: авторизация выполнена.")