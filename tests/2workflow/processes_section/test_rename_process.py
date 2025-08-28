import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_rename_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность действия Переименовать процесс."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Начало проверки Переименования процесса")
    workflows_page.right_click_and_select_action(process_name, "Переименовать")
    workflows_page.send_rename(process_name, f'RENAMED_{process_name}')

    refresh_and_wait(admin_driver, logger)
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")

    assert workflows_page.find_file_by_name(f'RENAMED_{process_name}'), f"Процесс 'RENAMED_{process_name}' не найден"
    workflows_page.right_click_and_select_action(f'RENAMED_{process_name}', "Переименовать")
    workflows_page.send_rename("", process_name)