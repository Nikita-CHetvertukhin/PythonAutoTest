import pytest  # Импорт библиотеки для работы с тестами
from pages.login_page import LoginPage
from locators.login_locators import LoginLocators
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue  # Декоратор для обработки исключений
from settings.variables import Admin_Login, Admin_Password  # Данные для тестирования авторизации

@pytest.mark.smoke  # Маркируем тест
@pytest.mark.parametrize("test_suite", [
    # Параметризованные тесты для проверки различных сценариев авторизации
    ("Некорректный логин", Admin_Login + "123", Admin_Password, True),  # Ожидаем ошибку из-за неверного логина
    ("Некорректный пароль", Admin_Login, Admin_Password + "123", True),  # Ожидаем ошибку из-за неверного пароля
    ("Успешная авторизация", Admin_Login, Admin_Password, False)  # Ожидаем успешную авторизацию без ошибок
])
@exception_handler  # Декоратор для обработки исключений во время выполнения теста
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
        if not login_page.check_error(expect_error, LoginLocators.AUTH_ERROR):
            error_handler.handle_exception(MinorIssue("Отсутствие ошибки при попытке входа с неверным логином/паролем"))
        assert not login_page.check_account_button(), "Элемент личного кабинета найден. Авторизация выполнена."
        logger.info(f"Тест '{suite_name}' завершён")
    else:
        # Проверяем наличие элемента личного кабинета + отсутствие любых ошибок
        assert login_page.check_account_button(), "Элемент личного кабинета не найден. Авторизация не удалась."
        if not login_page.check_error(expect_error):
            error_handler.handle_exception(MinorIssue("Присутствует ошибка при успешной авторизации"))
        logger.info(f"Тест '{suite_name}' завершился успешно: авторизация выполнена.")