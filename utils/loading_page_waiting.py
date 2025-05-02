# Импортируем необходимые классы из Selenium для работы с ожиданиями
from selenium.webdriver.support.ui import WebDriverWait  # Позволяет реализовать ожидание элементов
from selenium.webdriver.support import expected_conditions as EC  # Набор условий для WebDriverWait
from selenium.common.exceptions import TimeoutException  # Исключение, возникающее при превышении времени ожидания

class PageHandler:
    """Класс для управления загрузкой страницы и ожидания её полной готовности."""
    def __init__(self, logger, driver):
        """Инициализация объекта PageHandler.
        :param logger: Экземпляр логгера для записи событий.
        :param driver: Экземпляр WebDriver для управления браузером.
        """
        self.logger = logger  # Сохраняем переданный логгер
        self.driver = driver  # Сохраняем WebDriver

    def wait_for_page_to_load(self, timeout=10):
        """Ожидание полной загрузки страницы, используя `document.readyState`.
        :param timeout: Максимальное время ожидания загрузки страницы (в секундах).
        :return: `True`, если страница загрузилась успешно, иначе `False`.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"  # Ожидаем состояние `complete`
            )
            self.logger.info("Страница полностью загружена.")  # Логируем успешную загрузку
            return True
        except TimeoutException:
            self.logger.error(f"Страница не загрузилась за {timeout} секунд.")  # Логируем таймаут загрузки
            return False
        except Exception as e:
            self.logger.error(f"Ошибка загрузки страницы: {e}")  # Логируем любую другую ошибку
            return False