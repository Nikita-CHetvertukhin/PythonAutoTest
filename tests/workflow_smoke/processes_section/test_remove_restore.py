import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler

@pytest.mark.parametrize("setup_create_delete_process", [{
    "skip_cleanup": True
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_restore(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность действия 'Переместить в Корзину','Восстановление' и 'Окончательное удаление'."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Начало проверки удаления/восстановления процесса")
    workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
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