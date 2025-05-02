import pytest  # Фреймворк для тестирования Python
import sys  # Доступ к системным параметрам и настройкам интерпретатора
import logging  # Модуль для логирования событий, ошибок и сообщений отладки
import allure  # Интеграция с Allure для отчётов и вложений тестов
import time  # Работа с временными метками, задержками и вычислением времени выполнения
from pathlib import Path  # Удобная работа с путями файлов и каталогов
import functools

# Класс для обработки ошибок
class ErrorHandler:
    """Класс для обработки ошибок, логирования и создания скриншотов с интеграцией Allure.
    """
    def __init__(self, driver, logger=None):
        """Инициализация ErrorHandler.

        :param driver: WebDriver для работы с браузером.
        :param logger: Логгер для записи ошибок. Если не передан, создаётся новый.
        """
        self.driver = driver
        self.logger = logger  or logging.getLogger(__name__)

    def handle_exception(self, exception, screenshot_name=None):
        """
        Обрабатывает исключение: сохраняет скриншот, логирует ошибку и прикрепляет к отчету Allure.
    
        :param exception: Текст ошибки или исключение.
        :param screenshot_name: Имя файла скриншота (по умолчанию генерируется автоматически).
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = Path("log/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / (screenshot_name or f"screenshot_{timestamp}.png")

        self.driver.save_screenshot(screenshot_path)
        self.logger.warning(f"Ошибка: {exception}. Скриншот сохранён: {screenshot_path}")

        # Прикрепление скриншота к Allure
        if "pytest" in sys.modules:
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Ошибка: {exception}", attachment_type=allure.attachment_type.PNG)

