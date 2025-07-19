import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_copy_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность копирования нового процесса через контекстное меню."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Начало проверки открытия процесса")
    workflows_page.right_click_and_select_action(process_name, "Копировать")
    workflows_page.copy_to(f'COPY_{process_name}')

    workflows_page.click_header_logo_button()
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    
    assert workflows_page.find_process_by_name(f'COPY_{process_name}'), "Копия процесса не найдена"
