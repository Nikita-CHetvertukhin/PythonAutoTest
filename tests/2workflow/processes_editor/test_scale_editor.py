import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage
import allure

@allure.severity(allure.severity_level.NORMAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_scale_editor(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет создание, перемещение и соединение фигур в редактоер Workflow."""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки фигур WF в редакторе")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    shape = workflow_editor_page.add_shape("Вход") # Создание фигуры
    assert workflow_editor_page.adjust_zoom_and_verify("Приблизить", shape)
    assert workflow_editor_page.adjust_zoom_and_verify("Отдалить", shape)
    assert workflow_editor_page.adjust_zoom_and_verify("Автомасштаб", shape)