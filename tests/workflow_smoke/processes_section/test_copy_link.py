import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler

@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_copy_link(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность действия 'Скопировать ссылку'."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Начало проверки открытия процесса")
    workflows_page.right_click_and_select_action(process_name, "Скопировать ссылку")
    time.sleep(0.5)  # Даём браузеру записать ссылку в буфер
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться
    
    assert workflows_page.compare_clipboard_with_url(), "Ссылка в буфере не равно ссылке на процесс"
