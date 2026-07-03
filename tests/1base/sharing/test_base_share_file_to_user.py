import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import USER1_LOGIN
from utils.licence_checker import is_licence_enabled
from settings.variables import SHARING_INNER
from pages.my_files_page import MyFilesPage
import allure

@allure.severity(allure.severity_level.NORMAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.combo
@pytest.mark.skipif(
    not is_licence_enabled(SHARING_INNER),
    reason=f"Лицензия '{SHARING_INNER}' отключена — тест пропущен"
)
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новый документ"
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
@allure.epic('Коробка')
@allure.feature('Доступы')
@allure.title('Шеринг файла на УЗ')
def test_base_share_file_to_user(error_handler, logger, admin_driver, user1_driver, setup_create_delete_file):
    """Тест проверяет базовую возможность шеринга файла на УЗ (без проверки самого доступа)."""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_user1 = MyFilesPage(user1_driver, logger)

    logger.info("Начало проверки базовой возможности шеринга файла на УЗ")
    my_files_page.right_click_and_select_action(file_name,"Настроить доступ")
    my_files_page.share_access(action="set",logins_and_access=[(USER1_LOGIN, "Полный доступ")], is_close=False)
    # Ожидаем появления пошеренного процесса на УЗ
    time.sleep(2) # Пока ожидание явное, потом ожидание всплывающего уведомления
    my_files_user1.find_click_header_menu("Документы")
    my_files_user1.find_click_side_menu("Доступные мне")
    share_file = my_files_user1.find_file_by_name(file_name)
    if not share_file:
        logger.error(f"Файл '{file_name}' не найден у '{USER1_LOGIN}'")
        pytest.fail(f"Тест провален. Файл '{file_name}' не найден у '{USER1_LOGIN}'", pytrace=False)
    else:
        logger.info(f"Файл '{file_name}' успешно пошерен и найден у '{USER1_LOGIN}'.")

    logger.info("Начало проверки уровня 'Нет доступа'")
    my_files_page.share_access(action="edit", logins_and_access=[(USER1_LOGIN, "Нет доступа")])

    # Ожидаем отсутствия пошеренного документа на УЗ
    time.sleep(2) # Пока ожидание явное, потом ожидание всплывающего уведомления
    my_files_user1.click_header_logo_button()
    my_files_user1.find_click_header_menu("Документы")
    my_files_user1.find_click_side_menu("Доступные мне")
    share_file = my_files_user1.find_file_by_name(file_name)

    if share_file:
        logger.error(f"Ошибка. Файл '{file_name}' найден у '{USER1_LOGIN}', хотя он должен отсутствовать после отмены прав")
        pytest.fail(f"Тест провален. Файл '{file_name}' найден у '{USER1_LOGIN}'", pytrace=False)
    else:
        logger.info(f"Права доступа успешно отменены '{file_name}'")