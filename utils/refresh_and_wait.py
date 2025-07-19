import time
from selenium.webdriver.support.ui import WebDriverWait
from settings.variables import WEBSOCKET_PATCH

def refresh_and_wait(driver, logger=None, timeout=10):
    """Перезагружает страницу и ждет полной загрузки."""
    if logger:
        logger.info("Перезагрузка страницы...")

    time.sleep(1)  # Дополнительная задержка для полной инициализации страницы

    driver.refresh()

    # Ожидание полной загрузки страницы
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Отключаем вебсокеты для повышения стабильности тестов в ФС
    driver.execute_script(WEBSOCKET_PATCH)

    if logger:
        logger.info("Страница полностью загружена.")