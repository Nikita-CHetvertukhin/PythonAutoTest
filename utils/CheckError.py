from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.Errors import error_btnClose
import os
import time


class CheckError:
    """
    Класс для проверки наличия или отсутствия элемента ошибки.
    """

    def __init__(self, find=True, path=None):
        """
        Инициализация класса CheckError.

        :param find: True, если ожидается наличие элемента ошибки; False, если элемент ошибки не должен быть найден.
        :param path: XPath элемента ошибки. Если не указан, используется путь по умолчанию.
        """
        self.find = find
        self.path = path or "//div[contains(@class, 'error')]"  # Устанавливаем путь по умолчанию

    def check(self, driver, error_handler=None, timeout=1):
        """
        Проверяет наличие или отсутствие элемента ошибки и фиксирует результат.

        :param driver: WebDriver для взаимодействия с браузером.
        :param error_handler: Экземпляр Error_Handler для обработки ошибки (может быть None).
        :param timeout: Максимальное время ожидания элемента видимым (в секундах).
        :return: bool - True, если результат соответствует ожиданиям; False в противном случае.
        """
        try:
            # Ожидаем появления элемента ошибки
            error_element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.path))
            )

            # Если элемент найден
            if self.find:
                print(f"Успех: Ошибка найдена — {self.path}")
                self._click_close_button(driver)  # Закрываем элемент ошибки
                return True
            else:
                print(f"Провал: Ошибка не должна быть на странице — {self.path}")
                self._handle_error(driver, error_handler, f"Элемент ошибки найден — {self.path}")
                return False

        except TimeoutException:
            return self._handle_timeout(driver, error_handler)

        except NoSuchElementException:
            return self._handle_no_element(driver, error_handler)

    def _click_close_button(self, driver):
        """
        Находит кнопку "Закрыть" и выполняет клик.

        :param driver: WebDriver для взаимодействия с браузером.
        """
        try:
            close_button = driver.find_element(By.XPATH, error_btnClose)
            close_button.click()
            print(f"Кнопка 'Закрыть' была нажата.")
        except NoSuchElementException:
            print(f"Ошибка: Кнопка 'Закрыть' не найдена — {error_btnClose}")

    def _handle_error(self, driver, error_handler, exception_message):
        """
        Логирует и фиксирует ошибку.

        :param driver: WebDriver для взаимодействия с браузером.
        :param error_handler: Экземпляр Error_Handler для обработки ошибки.
        :param exception_message: Описание ошибки.
        """
        if error_handler:
            # Генерируем уникальное имя скриншота
            screenshot_name = self._generate_screenshot_name("error_found")
            error_handler.handle_exception(
                exception=exception_message,
                screenshot_name=screenshot_name
            )
        self._click_close_button(driver)

    def _handle_timeout(self, driver, error_handler):
        """
        Обрабатывает случай таймаута ожидания элемента.

        :param driver: WebDriver для взаимодействия с браузером.
        :param error_handler: Экземпляр Error_Handler для обработки ошибки.
        :return: bool - True, если ожидание таймаута соответствует find=False; False в противном случае.
        """
        if self.find:
            print(f"Провал: Элемент ошибки не стал видимым — {self.path}")
            if error_handler:
                screenshot_name = self._generate_screenshot_name("timeout_error")
                error_handler.handle_exception(
                    exception=f"Элемент ошибки не отображён корректно — {self.path}",
                    screenshot_name=screenshot_name
                )
            return False
        else:
            print(f"Успех: Элемент ошибки не обнаружен на странице — {self.path}")
            return True

    def _handle_no_element(self, driver, error_handler):
        """
        Обрабатывает случай отсутствия элемента ошибки.

        :param driver: WebDriver для взаимодействия с браузером.
        :param error_handler: Экземпляр Error_Handler для обработки ошибки.
        :return: bool - True, если отсутствие элемента соответствует find=False; False в противном случае.
        """
        if self.find:
            print(f"Провал: Элемент ошибки не найден, но должен быть — {self.path}")
            if error_handler:
                screenshot_name = self._generate_screenshot_name("no_such_element_error")
                error_handler.handle_exception(
                    exception=f"Элемент ошибки не найден, но его наличие ожидалось — {self.path}",
                    screenshot_name=screenshot_name
                )
            return False
        else:
            print(f"Успех: Элемент ошибки отсутствует на странице — {self.path}")
            return True

    def _generate_screenshot_name(self, error_type):
        """
        Генерирует уникальное имя для скриншота.

        :param error_type: Тип ошибки (например, 'error_found', 'timeout_error').
        :return: Строка с уникальным именем для скриншота.
        """
        # # Папка для сохранения скриншотов
        # log_dir = "log/screenshots"
        # os.makedirs(log_dir, exist_ok=True)  # Создаем папку, если её нет

        # # Генерация имени на основе времени и типа ошибки
        # timestamp = time.strftime("%Y%m%d_%H%M%S")
        # return os.path.join(log_dir, f"{error_type}_{timestamp}.png")