# Глобальный импорт
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Локальный импорт
from settings.Variables import URL  # URL берётся из config

class BrowserDriver:
    def __init__(self, browser_type="chrome"):
        self.browser_type = browser_type.lower()
        self.url = URL  # Предполагаем, что URL импортирован
        self.driver = None

    def initialize_driver(self):
        if self.browser_type == "chrome":
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
        elif self.browser_type == "firefox":
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service)
        else:
            raise ValueError(f"Браузер '{self.browser_type}' не поддерживается")

        self.driver.get(self.url)  # Переход по URL
        return self.driver
