import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage

@pytest.fixture
def setup_test_remove_restore(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_page = WorkflowsPage(admin_driver, logger)
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

    workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
    
    return process_name, workflows_page

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_restore(error_handler, logger, admin_driver, setup_test_remove_restore):
    """Тест проверяет возможность действия 'Переместить в Корзину','Восстановление' и 'Окончательное удаление'."""
    process_name, workflows_page = setup_test_remove_restore

    logger.info("Начало проверки восстановления процесса")
    workflows_page.find_click_side_menu("Корзина")
    time.sleep(1)
    workflows_page.find_process_by_name(process_name)
    workflows_page.right_click_and_select_action(process_name, "Восстановить")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    time.sleep(1)
    assert workflows_page.find_process_by_name(process_name), f"Процесс {process_name} не найден после восстановления"
    logger.info(f"Процесс '{process_name}' успешно восстановлен.")

    workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
    workflows_page.find_click_side_menu("Корзина")
    workflows_page.right_click_and_select_action(process_name, "Удалить навсегда")
    workflows_page.dialog_window(True)
    time.sleep(1)
    assert not workflows_page.find_process_by_name(process_name), f"Процесс {process_name} найден после удаления навсегда"