import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize("setup_create_delete_process", [{
    "skip_cleanup": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_remove_restore(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность действия 'Переместить в Корзину','Восстановление' и 'Окончательное удаление'."""
    process_name, workflows_page, xpath = setup_create_delete_process

    logger.info("Начало проверки удаления/восстановления процесса")
    workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
    time.sleep(1) #Даём файлу время на исчезновение из раздела
    workflows_page.find_click_side_menu("Корзина")
    workflows_page.find_file_by_name(process_name)
    workflows_page.right_click_and_select_action(process_name, "Восстановить")
    time.sleep(1) #Даём файлу время на исчезновение из раздела
    workflows_page.find_click_side_menu("Шаблоны процессов")
    assert workflows_page.find_file_by_name(process_name), f"Процесс {process_name} не найден после восстановления"
    logger.info(f"Процесс '{process_name}' успешно восстановлен.")

    workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
    time.sleep(1) #Даём файлу время на исчезновение из раздела
    workflows_page.find_click_side_menu("Корзина")
    workflows_page.right_click_and_select_action(process_name, "Удалить навсегда")
    workflows_page.dialog_window(True)
    time.sleep(1) #Даём файлу время на исчезновение из раздела
    assert not workflows_page.find_file_by_name(process_name), f"Процесс {process_name} найден после удаления навсегда"