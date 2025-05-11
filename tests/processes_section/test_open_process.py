import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage

@pytest.fixture
def setup_test_open_process(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_page = WorkflowsPage(admin_driver, logger)
    process_name = workflows_page.generate_object_name()

    logger.info("Создание процесса...")
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    workflows_page.create_process(process_name)

    # Проверяем, что процесс действительно создался
    if not workflows_page.find_process_by_name(process_name):
        logger.error(f"Ошибка: процесс '{process_name}' не был создан!")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не был создан.", pytrace=False)

    def cleanup():
        """Удаление процесса после теста."""
        logger.info(f"Удаление процесса '{process_name}'...")
        time.sleep(2)  # Ждём явно, пока не появятся статусы сохранения
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        process_to_delete = workflows_page.find_process_by_name(process_name)
        if process_to_delete:
            workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page

@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_open_process(error_handler, logger, admin_driver, setup_test_open_process):
    """Тест проверяет возможность открытия нового процесса через контекстное меню или двойным ЛКМ."""
    process_name, workflows_page = setup_test_open_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки открытия процесса")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    check_open = workflow_editor_page.verify_process_name(process_name)  # Проверяем, что открылся нужный процесс

    if not check_open:
        logger.error(f"Ошибка: процесс '{process_name}' не открылся корректно.")
        pytest.fail(f"Тест провален. Открытие процесса '{process_name}' не удалось.", pytrace=False)
    else:
        logger.info(f"Процесс '{process_name}' успешно открыт через контекстное меню и двойным кликом.")