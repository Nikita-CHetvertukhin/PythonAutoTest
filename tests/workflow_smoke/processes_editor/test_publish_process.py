import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_publish_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет публикацию и снятие с публикации процесса."""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Начало проверки публикации процесса")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    workflow_editor_page.action_from_document("Опубликовать")
    time.sleep(2) # Пока не на что опираться в редакторе
    workflows_page.find_click_header_menu("Мои задачи")
    time.sleep(1) # Пока не проверяю запросы и не жду часиков
    assert my_tasks_page.checking_publish_process(process_name)

    logger.info("Начало проверки снятия с публикации процесса")
    refresh_and_wait(admin_driver, logger)
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    time.sleep(1) # Пока не проверяю запросы и не жду часиков
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться
    workflow_editor_page.action_from_document("Снять с публикации")
    time.sleep(2) # Пока не на что опираться в редакторе
    workflows_page.find_click_header_menu("Мои задачи")
    time.sleep(2) # Пока не проверяю запросы и не жду часиков
    assert not my_tasks_page.checking_publish_process(process_name)