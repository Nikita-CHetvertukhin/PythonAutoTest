import pytest  # Фреймворк для тестирования Python
import sys  # Доступ к системным параметрам и настройкам интерпретатора
import logging  # Модуль для логирования событий, ошибок и сообщений отладки
import allure  # Интеграция с Allure для отчётов и вложений тестов
import time  # Работа с временными метками, задержками и вычислением времени выполнения
from pathlib import Path
import uuid
from utils.refresh_and_wait import refresh_and_wait

from selenium.common.exceptions import WebDriverException
# Класс для обработки ошибок
class ErrorHandler:
    """Класс для обработки ошибок, логирования и создания скриншотов с интеграцией Allure.
    """
    def __init__(self, driver, logger=None, browser_type="chrome"):
        """Инициализация ErrorHandler.

        :param driver: WebDriver для работы с браузером.
        :param logger: Логгер для записи ошибок. Если не передан, создаётся новый.
        """
        self.driver = driver
        self.logger = logger  or logging.getLogger(__name__)
        self.browser_type = browser_type.strip().lower()

    def handle_exception(self, exception, screenshot_name=None, critical=True):
        """
        Обрабатывает исключение: сохраняет скриншот, логирует ошибку и прикрепляет к отчету Allure.
    
        :param exception: Текст ошибки или исключение.
        :param screenshot_name: Имя файла скриншота (по умолчанию генерируется автоматически).
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]  # Например: a3b7f9c1
        screenshot_dir = Path("log/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / (screenshot_name or f"{unique_id}_screenshot_{timestamp}.png")

        self.driver.save_screenshot(screenshot_path)
        self.logger.error(f"Ошибка: {exception}. Скриншот сохранён: {screenshot_path}")

        # Прикрепление скриншота к Allure
        if "pytest" in sys.modules:
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Ошибка: {exception}", attachment_type=allure.attachment_type.PNG)

        # Если ошибка критическая - обновляем страницу
        if critical:
            refresh_and_wait(self.driver, self.logger)

    def check_browser_logs(self):
        """Проверяет консоль браузера и прикрепляет скриншот и ошибки в Allure при наличии SEVERE-сообщений."""
        if self.browser_type == "firefox":
            self.logger.debug("Пропускаем сбор логов — Firefox не поддерживает get_log('browser').")
            return
        try:
            logs = self.driver.get_log("browser")
            errors = [entry for entry in logs if entry["level"] == "SEVERE"]
            if errors:
                error_messages = "\n".join(f"[{e['timestamp']}] {e['message']}" for e in errors)

                # Сохраняем скриншот текущего состояния страницы
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                unique_id = uuid.uuid4().hex[:8]  # Например: a3b7f9c1
                screenshot_dir = Path("log/screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshot_dir / f"console_error_{unique_id}_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.error("Обнаружены ошибки в консоли браузера:\n" + error_messages)
                self.logger.error(f"Скриншот сохранён: {screenshot_path}")

                # Прикрепляем текст ошибок и скриншот к Allure
                if "pytest" in sys.modules:
                    allure.attach(error_messages, name="Ошибки в консоли", attachment_type=allure.attachment_type.TEXT)
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(image_file.read(), name="Скриншот при ошибке в консоли", attachment_type=allure.attachment_type.PNG)

                pytest.fail("Обнаружены ошибки в консоли браузера:\n" + error_messages)

        except WebDriverException as e:
            self.logger.warning(f"Не удалось получить логи из браузера: {e}")

    def clear_browser_logs(self):
        """Очищает текущие логи браузера, чтобы не мешали анализу новых ошибок."""
        if self.browser_type == "firefox":
            self.logger.debug("Пропускаем сбор логов — Firefox не поддерживает get_log('browser').")
            return
        try:
            # Просто считываем все текущие логи, чтобы их сбросить и далее учитывать только новые
            self.driver.get_log("browser")
            self.logger.debug("Консоль браузера очищена перед выполнением теста.")
            time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Не удалось очистить логи браузера: {e}")
