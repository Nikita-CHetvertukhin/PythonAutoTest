"""Отслеживает driver, использованный последним в XPathFinder.

Нужен, чтобы в combo-тестах (несколько УЗ/браузеров в одном потоке) error_handler
брал скриншот/URL с того окна, где реально произошла ошибка, а не всегда с
основного (admin) driver, к которому он привязан по умолчанию. Тесты выполняются
последовательно в одном потоке, поэтому простой module-level переменной достаточно —
блокировка не нужна. Между xdist-воркерами эта переменная не шарится, т.к. каждый
воркер — отдельный процесс с собственной памятью.
"""

_active_driver = None


def set_active_driver(driver):
    global _active_driver
    _active_driver = driver


def get_active_driver():
    return _active_driver
