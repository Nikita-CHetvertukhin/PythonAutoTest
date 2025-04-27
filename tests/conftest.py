#Глобальный импорт
import pytest
#Локальный импорт
from utils.BrowserDriver import BrowserDriver
from settings.Variables import Browser

@pytest.fixture(scope="session")
def driver():
    driver_instance = BrowserDriver(browser_type=Browser)
    driver = driver_instance.initialize_driver()

    yield driver  # Передаём драйвер в тесты

    # Закрытие драйвера после выполнения всех тестов
    driver.quit()
