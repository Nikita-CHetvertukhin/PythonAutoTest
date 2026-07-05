import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from settings.variables import WEBSOCKET_PATCH

def refresh_and_wait(driver, logger=None, timeout=10):
    """Перезагружает страницу и ждет полной загрузки."""
    if logger:
        logger.info("Перезагрузка страницы...")

    time.sleep(1)  # Дополнительная задержка для полной инициализации страницы

    driver.refresh()

    # Ожидание полной загрузки страницы. Не считаем это фатальным: если readyState
    # не дошёл до "complete" за timeout (например, из-за фоновой сетевой активности SPA),
    # продолжаем — последующие шаги теста сами упадут с информативной ошибкой,
    # если страница реально не готова к работе.
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        if logger:
            logger.info("Страница полностью загружена.")
    except TimeoutException:
        if logger:
            logger.warning(f"document.readyState не стал 'complete' за {timeout}с после обновления страницы — продолжаем без ожидания.")

    # Отключаем вебсокеты для повышения стабильности тестов в ФС
    driver.execute_script(WEBSOCKET_PATCH)

    time.sleep(3)  # Дополнительная задержка для полной инициализации страницы