from selenium.webdriver.support.ui import WebDriverWait

def refresh_and_wait(driver, logger=None, timeout=10):
    """Перезагружает страницу и ждет полной загрузки."""
    if logger:
        logger.info("Перезагрузка страницы...")

    driver.refresh()

    # Ожидание полной загрузки страницы
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    if logger:
        logger.info("Страница полностью загружена.")