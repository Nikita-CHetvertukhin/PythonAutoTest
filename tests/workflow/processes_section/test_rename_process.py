import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.fixture
def setup_test_rename_process(request, logger, admin_driver):
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
        logger.info(f"Удаление процесса 'RENAMED_{process_name}'...")
        process_to_delete = workflows_page.find_process_by_name(f'RENAMED_{process_name}')
        if process_to_delete:
            workflows_page.right_click_and_select_action(f'RENAMED_{process_name}', "Переместить в Корзину")
            logger.info(f"Процесс 'RENAMED_{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс 'RENAMED_{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_rename_process(error_handler, logger, admin_driver, setup_test_rename_process):
    """Тест проверяет возможность действия Переименовать процесс."""
    process_name, workflows_page = setup_test_rename_process

    logger.info("Начало проверки Переименования процесса")
    workflows_page.right_click_and_select_action(process_name, "Переименовать")
    workflows_page.send_rename(process_name, f'RENAMED_{process_name}')

    refresh_and_wait(admin_driver, logger)
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")

    assert workflows_page.find_process_by_name(f'RENAMED_{process_name}'), f"Процесс 'RENAMED_{process_name}' не найден"