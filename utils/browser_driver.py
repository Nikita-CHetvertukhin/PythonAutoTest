from selenium import webdriver  # Основной модуль Selenium для управления браузерами
from selenium.webdriver.chrome.service import Service  # Оптимизированный способ запуска Chrome WebDriver
from webdriver_manager.chrome import ChromeDriverManager  # Автоматическое управление версией Chrome WebDriver

from settings.variables import URL  # URL загружается из конфигурационного файла

class BrowserDriver:
    """Класс для управления веб-драйвером, поддерживающим Chrome и Firefox."""
    def __init__(self, browser_type="chrome"):
        """:param browser_type: Тип браузера для инициализации ("chrome" или "firefox")."""
        self.browser_type = browser_type.lower()  # Приведение названия браузера к нижнему регистру для унификации
        self.url = URL  # URL веб-приложения, полученный из конфигурации
        self.driver = None  # Экземпляр WebDriver будет создан в `initialize_driver()`

    def initialize_driver(self):
        """Инициализация WebDriver в зависимости от указанного типа браузера."""
        if self.browser_type == "chrome":
            service = Service(ChromeDriverManager().install())  # Установка и управление Chrome WebDriver
            options = webdriver.ChromeOptions()  # Опции для Chrome (можно добавить параметры, например headless)
            self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser_type == "firefox":
            options = webdriver.FirefoxOptions()  # Опции для Firefox (можно добавить параметры, например headless)
            self.driver = webdriver.Firefox(options=options)  # Firefox сам управляет запуском WebDriver

        else:
            raise ValueError(
                f"Браузер '{self.browser_type}' не поддерживается. Допустимые варианты: 'chrome', 'firefox'."
            )  # Обработка ошибки, если браузер неизвестен

        self.driver.get(self.url)  # Открытие указанного URL после инициализации браузера
        return self.driver  # Возвращает объект WebDriver для дальнейшей работы