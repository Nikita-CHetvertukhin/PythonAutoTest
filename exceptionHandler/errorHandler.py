import allure  # Интеграция с Allure для отчётов и вложений
import time  # Работа с временными метками
from logging.handlers import RotatingFileHandler  # Ротация логов для управления файлами
import os  # Работа с файловой системой

# Класс для обработки ошибок
class ErrorHandler:
    """
    Класс для обработки ошибок, логирования и создания скриншотов с интеграцией Allure.
    """

    def __init__(self, driver, logger=None):
        """
        Инициализация ErrorHandler.

        :param driver: WebDriver для работы с браузером.
        :param logger: Логгер для записи ошибок. Если не передан, создаётся новый.
        """
        self.driver = driver
        self.logger = logger

    def capture_screenshot(self, name=None):
        """
        Создаёт скриншот текущего состояния браузера.

        :param name: Имя файла скриншота. Если не передано, генерируется уникальное имя.
        :return: Путь к сохранённому скриншоту.
        """
        # Папка для скриншотов
        screenshot_dir = "log/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)  # Создаём папку, если её нет

        # Генерация уникального имени для скриншота
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_name = name or f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)

        # Сохраняем скриншот
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Скриншот сохранён: {screenshot_path}")
        return screenshot_path

    def attach_to_allure(self, exception, screenshot_path):
        """
        Прикрепляет скриншот и описание ошибки к отчёту Allure.

        :param exception: Исключение или описание ошибки.
        :param screenshot_path: Путь к скриншоту.
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Ошибка: {exception}",
            attachment_type=allure.attachment_type.PNG
        )

    def handle_exception(self, exception, screenshot_name=None):
        """
        Обрабатывает исключение: сохраняет скриншот, логирует и интегрирует в Allure.

        :param exception: Исключение или описание ошибки.
        :param screenshot_name: Имя файла для скриншота ошибки.
        """
        screenshot_path = self.capture_screenshot(screenshot_name)
        self.attach_to_allure(exception, screenshot_path)
        self.logger.error(f"Ошибка: {exception}. Скриншот прикреплён к Allure.")