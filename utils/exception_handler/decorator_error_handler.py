import functools
import allure
import pytest

class MinorIssue(Exception):
    """Некритическая ошибка, тест продолжается."""
    pass

def exception_handler(func):
    """Декоратор для обработки исключений, классификации и логирования через ErrorHandler."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        error_handler = kwargs.get("error_handler")
        if error_handler is None:
            raise ValueError("Фикстура `error_handler` не передана! Проверьте тестовую среду.")

        try:
            result = func(*args, **kwargs)
            error_handler.check_browser_logs()  # Проверяем логи браузера на наличие ошибок.
            return result

        except MinorIssue as e:
            with allure.step("Некритическая ошибка"):
                error_handler.handle_exception(e, critical=False)  # Логируем и создаем скриншотб не перезагружаю старницу
                pytest.mark.xfail(run=True, reason=f"Обработанная некритическая ошибка: {e}")

        except Exception as e:
            error_handler.handle_exception(e)  # Логируем и создаем скриншот
            raise

    return wrapper