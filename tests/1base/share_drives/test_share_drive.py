import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from utils.refresh_and_wait import refresh_and_wait
from utils.licence_checker import is_licence_enabled
from settings.variables import SHARE_DRIVES
from settings.variables import USER1_LOGIN
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.combo
@pytest.mark.skipif(
    not is_licence_enabled(SHARE_DRIVES),
    reason=f"Лицензия '{SHARE_DRIVES}' отключена — тест пропущен"
)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_share_drive(error_handler, logger, admin_driver, user1_driver, setup_create_delete_drive):
    """Тест проверяет базовую возможность шеринга общего диска"""
    drive_name, my_files_page, xpath = setup_create_delete_drive
    user1_my_files_page = MyFilesPage(user1_driver, logger)

    logger.info("Начало проверки базового шеринга общего диска")
    # Настройки доступа
    my_files_page.right_click_and_select_action(drive_name, "Настроить доступ")
    my_files_page.share_access(f"{USER1_LOGIN}", "Полный доступ")
    # Ожидаем появления пошеренного процесса на УЗ
    time.sleep(2) # Пока ожидание явное, потом ожидание всплывающего уведомления
    user1_my_files_page.find_click_header_menu("Документы")
    user1_my_files_page.find_click_side_menu("Общие диски")
    share_drive = user1_my_files_page.find_file_by_name(drive_name)
    if not share_drive:
        logger.error(f"Диск '{share_drive}' не найден у '{USER1_LOGIN}'")
        pytest.fail(f"Тест провален. Диск '{share_drive}' не найден у '{USER1_LOGIN}'", pytrace=False)
    else:
        logger.info(f"Диск '{share_drive}' успешно пошерен и найден у '{USER1_LOGIN}'.")