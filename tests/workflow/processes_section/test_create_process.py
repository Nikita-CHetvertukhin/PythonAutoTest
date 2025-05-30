import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from utils.refresh_and_wait import refresh_and_wait
from pages.workflows_page import WorkflowsPage
from locators.workflows_locators import WorkflowsLocators

@pytest.fixture
def setup_test_create_process(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_page = WorkflowsPage(admin_driver, logger)
    process_name = workflows_page.generate_object_name()

    logger.info("Создание процесса...")
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    workflows_page.create_process(process_name)

    if not workflows_page.find_process_by_name(process_name):
        logger.error(f"Ошибка: процесс '{process_name}' не был создан!")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не был создан.", pytrace=False)

    def cleanup():
        """Удаление процесса после теста."""
        logger.info(f"Удаление процесса '{process_name}'...")
        time.sleep(0.5)
        process_to_delete = workflows_page.find_process_by_name(process_name)
        if process_to_delete:
            workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_process(error_handler, logger, admin_driver, setup_test_create_process):
    """Тест проверяет возможность создания нового процесса, присваивание ему имени и доступность после перезагрузки страницы."""
    process_name, workflows_page = setup_test_create_process

    logger.info("Проверяем наличие созданного процесса")
    workflows_page.click_header_logo_button()
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    current_process = workflows_page.find_process_by_name(process_name)

    if not current_process:
        logger.error(f"Процесс '{process_name}' не найден после создания.")
        error_handler.handle_exception(MinorIssue(f"Ошибка. Процесс '{process_name}' не найден после создания."))
        pytest.fail(f"Тест провален. Процесс '{process_name}' не найден после создания.", pytrace=False)
    else:
        logger.info(f"Процесс '{process_name}' успешно создан и найден.")