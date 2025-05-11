import pytest

from utils.exception_handler.decorator_error_handler import exception_handler
from locators.generation_locators import GenerationLocators
from pages.generation_page import GenerationPage

@pytest.mark.smoke
@exception_handler
def test_generateDatabaseSchema(error_handler, logger, admin_driver):
    """Тест на генерацию схемы базы данных."""
    generation_page = GenerationPage(admin_driver, logger)
    
    logger.info("Поиск кнопок по пути 'Администрирование' - 'Генерация схемы данных'")
    generation_page.find_click_header_menu("Администрирование", "Генерация схемы данных")

    assert generation_page.wait_for_100_percent(timeout=120), "Генерация схемы не выполнена"
    assert generation_page.check_error(False, GenerationLocators.GENERATION_ERROR, False), "Присутствуют ошибки при генерации схемы"
    logger.info("Генерация схемы данных завершена успешно")