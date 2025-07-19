import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_open_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность открытия нового процесса через контекстное меню или двойным ЛКМ."""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки открытия процесса")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    assert workflow_editor_page.verify_process_name(process_name), f"Ошибка: название '{process_name}' не найдено."