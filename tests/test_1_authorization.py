#Глобальный импорт
import pytest  # Импорт библиотеки для работы с тестами

# Локальный импорт
from pages.Signin import *  # Импорт всех элементов страницы авторизации
from pages.Header import header_btnUser  # Импорт элемента кнопки личного кабинета
from pages.Errors import error_txtCredentials  # Импорт элемента сообщения об ошибке авторизации (Неверный логин или пароль)
from utils.findeByXPath import finde_Xpath_visible, finde_Xpath_clickable  # Утилиты для работы с элементами по XPath
from utils.CheckError import CheckError  # Класс для проверки наличия всплывающих окон ошибок
from settings.Variables import Admin_Login, Admin_Password  # Данные для тестирования авторизации
from exceptionHandler.errorHandler import ErrorHandler  # Класс для обработки ошибок
from exceptionHandler.configureLogging import configure_logging
from exceptionHandler.Decorator import exception_handler

# Инициализация логгера
logger = configure_logging()

'''
@pytest.mark.parametrize Декоратор обеспечивающий многократный запуск теста с разными параметрами
test_suite это массив содержащий параметры теста:
    1. suite_name - название теста
    2. login - логин для авторизации
    3. password - пароль для авторизации
    4. expect_error - ожидаемая всплывающая ошибка (True - ошибка ожидается например при вводе неверных логин/пароля, False - ошибка не ожидалась при вводе верных данных)
'''
@pytest.mark.parametrize("test_suite", [
    ("Некорректный логин", Admin_Login + "123", Admin_Password, True),
    ("Некорректный пароль", Admin_Login, Admin_Password + "123", True),
    ("Успешная авторизация", Admin_Login, Admin_Password, False)
])
def test_authorization(driver, test_suite):
    # Инициализация обработчика ошибок
    error_handler = ErrorHandler(driver, logger)

    # Получение параметров из test_suite
    suite_name, login, password, expect_error = test_suite
    logger.info(f"Начало выполнения теста: {suite_name}")

    # Оборачиваем всё тело теста в декоратор, чтобы обработать ошибки
    @exception_handler(error_handler)
    def execute_test(driver, suite_name, login, password, expect_error):
        # Тестовая логика
        input_Login = finde_Xpath_visible(driver, signin_txtLogin)
        input_Password = finde_Xpath_visible(driver, signin_txtPassword)
        btnSignin = finde_Xpath_clickable(driver, signin_btnSignin)

        # Очистка полей и ввод данных
        input_Login.clear()
        input_Login.send_keys(login)
        input_Password.clear()
        input_Password.send_keys(password)
        btnSignin.click()

        # Проверка результатов
        result = CheckError(expect_error, error_txtCredentials).check(driver, error_handler)
        if expect_error:
            assert result, f"Ожидалась ошибка авторизации: {suite_name}"
            logger.info(f"Тест '{suite_name}' завершился успешно: ошибка авторизации подтверждена.")
        else:
            finde_Xpath_visible(driver, header_btnUser)
            assert result, "Ошибка не ожидалась при успешной авторизации."
            logger.info(f"Тест '{suite_name}' завершился успешно: авторизация выполнена.")
    # Запуск теста
    execute_test(driver, suite_name, login, password, expect_error)