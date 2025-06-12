import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from locators.workflows_locators import WorkflowsLocators
from settings.variables import USER1_LOGIN

@pytest.fixture
def setup_test_share_process(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_admin = WorkflowsPage(admin_driver, logger)
    process_name = workflows_admin.generate_object_name()

    logger.info("Создание процесса...")
    workflows_admin.find_click_header_menu("Рабочие процессы")
    workflows_admin.find_click_side_menu("Шаблоны процессов")
    time.sleep(1)  # Ждем, чтобы страница успела загрузиться Потом поправить на ожидание request
    workflows_admin.create_process(process_name)

    # Проверяем, что процесс действительно создался
    if not workflows_admin.find_process_by_name(process_name):
        logger.error(f"Ошибка: процесс '{process_name}' не был создан!")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не был создан.", pytrace=False)

    def cleanup():
        """Удаление процесса после теста."""
        logger.info(f"Удаление процесса '{process_name}'...")
        workflows_admin.find_click_header_menu("Рабочие процессы")
        workflows_admin.find_click_side_menu("Шаблоны процессов")
        process_to_delete = workflows_admin.find_process_by_name(process_name)
        if process_to_delete:
            workflows_admin.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_admin

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_share_process(error_handler, logger, admin_driver, user1_driver, setup_test_share_process):
    """Тест проверяет возможность шеринга процесса."""
    process_name, workflows_admin = setup_test_share_process
    workflows_user1 = WorkflowsPage(user1_driver, logger)

    logger.info("Начало проверки шеринга процесса")
    workflows_admin.right_click_and_select_action(process_name,"Настроить доступ")
    workflows_admin.share_access(f"{USER1_LOGIN}", "Редактор")

    # Ожидаем появления пошеренного процесса на УЗ
    time.sleep(2) # Пока ожидание явное, потом ожидание всплывающего уведомления
    workflows_user1.find_click_header_menu("Рабочие процессы")
    workflows_user1.find_click_side_menu("Шаблоны процессов")
    time.sleep(0.5)
    share_process = workflows_user1.find_process_by_name(process_name)
    if not share_process:
        logger.error(f"Процесс '{process_name}' не найден у '{USER1_LOGIN}'")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не найден у '{USER1_LOGIN}'", pytrace=False)
    else:
        logger.info(f"Процесс '{process_name}' успешно пошерен и найден у '{USER1_LOGIN}'.")
    workflows_user1.click_header_logo_button()

    logger.info("Начало проверки уровня 'Нет доступа'")
    workflows_admin.right_click_and_select_action(process_name, "Настроить доступ")
    workflows_admin.share_access(f"{USER1_LOGIN}", "Нет доступа")

    # Ожидаем отсутствия пошеренного процесса на УЗ
    time.sleep(2) # Пока ожидание явное, потом ожидание всплывающего уведомления
    workflows_user1.find_click_header_menu("Рабочие процессы")
    workflows_user1.find_click_side_menu("Шаблоны процессов")
    share_process = workflows_user1.find_process_by_name(process_name)

    if share_process:
        logger.error(f"Ошибка. Процесс '{process_name}' найден у '{USER1_LOGIN}', хотя он должен отсутствовать после отмены прав")
        pytest.fail(f"Тест провален. Процесс '{process_name}' найден у '{USER1_LOGIN}'", pytrace=False)
    else:
        logger.info(f"Права доступа успешно отменены '{process_name}'")