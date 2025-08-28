import pytest
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность создания нового процесса, присваивание ему имени и доступность после перезагрузки страницы."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Проверяем наличие созданного процесса")
    workflows_page.click_header_logo_button()
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    current_process = workflows_page.find_file_by_name(process_name)

    if not current_process:
        logger.error(f"Процесс '{process_name}' не найден после создания.")
        error_handler.handle_exception(MinorIssue(f"Ошибка. Процесс '{process_name}' не найден после создания."), critical=False)
        pytest.fail(f"Тест провален. Процесс '{process_name}' не найден после создания.", pytrace=False)
    else:
        logger.info(f"Процесс '{process_name}' успешно создан и найден.")