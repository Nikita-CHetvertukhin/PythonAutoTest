import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.fixture
def setup_test_copy_process(request, logger, admin_driver):
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
        logger.info(f"Удаление процесса '{process_name}' и 'COPY_{process_name}'...")
        refresh_and_wait(admin_driver, logger)
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        process_to_delete = workflows_page.find_process_by_name(process_name)
        copy_to_delete = workflows_page.find_process_by_name(f'COPY_{process_name}')
        time.sleep(0.5)
        if process_to_delete:
            workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")
        time.sleep(0.5)
        if copy_to_delete:
            workflows_page.right_click_and_select_action(f'COPY_{process_name}', "Переместить в Корзину")
            logger.info(f"Процесс 'COPY_{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс 'COPY_{process_name}' не найден для удаления.")
        
    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page

@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_copy_process(error_handler, logger, admin_driver, setup_test_copy_process):
    """Тест проверяет возможность копирования нового процесса через контекстное меню."""
    process_name, workflows_page = setup_test_copy_process

    logger.info("Начало проверки открытия процесса")
    workflows_page.right_click_and_select_action(process_name, "Копировать")
    workflows_page.copy_to(f'COPY_{process_name}')

    workflows_page.click_header_logo_button()
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    
    assert workflows_page.find_process_by_name(f'COPY_{process_name}'), "Копия процесса не найдена"
