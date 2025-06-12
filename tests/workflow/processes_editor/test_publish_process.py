import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.fixture
def setup_test_publish_process(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_page = WorkflowsPage(admin_driver, logger)
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    process_name = workflows_page.generate_object_name()

    logger.info("Создание процесса...")
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    time.sleep(1)  # Ждем, чтобы страница успела загрузиться Потом поправить на ожидание request
    workflows_page.create_process(process_name)

    # Проверяем, что процесс действительно создался
    if not workflows_page.find_process_by_name(process_name):
        logger.error(f"Ошибка: процесс '{process_name}' не был создан!")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не был создан.", pytrace=False)

    def cleanup():
        """Удаление процесса после теста."""
        logger.info(f"Удаление процесса '{process_name}'...")
        refresh_and_wait(admin_driver, logger)
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        process_to_delete = workflows_page.find_process_by_name(process_name)
        if process_to_delete:
            workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page, workflow_editor_page

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_publish_process(error_handler, logger, admin_driver, setup_test_publish_process):
    """Тест проверяет создание, перемещение и соединение фигур в редактоер Workflow."""
    process_name, workflows_page, workflow_editor_page = setup_test_publish_process
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Начало проверки фигур WF в редакторе")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    workflow_editor_page.action_from_document("Опубликовать")
    time.sleep(2) # Пока не на что опираться в редакторе
    workflows_page.find_click_header_menu("Мои задачи")
    time.sleep(1) # Пока не проверяю запросы и не жду часиков
    assert my_tasks_page.checking_publish_process(process_name)