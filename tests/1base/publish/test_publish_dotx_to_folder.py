import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from settings.variables import ADMIN_LOGIN
from utils.refresh_and_wait import refresh_and_wait
import allure
from utils.get_date import get_timestamp, get_uuid

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "folder_in_templates": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_publish_dotx_to_folder(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет публикацию шаблона в папку в разделе 'Шаблоны'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    dotx_name = f'test_publish_dotx_to_folder_{get_uuid()}_{get_timestamp()}'

    logger.info("Начало проверки публикации шаблона в папку")
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.create_file(dotx_name, "Интерактивный шаблон")
    my_files_page.right_click_and_select_action(dotx_name,"Открыть")
    my_files_editor_page.waiting_status_after("open")
    # Публикация в папку
    my_files_editor_page.click_file_and_click("Опубликовать")
    my_files_editor_page.publish_to(logins_groups=[f"{ADMIN_LOGIN}"], directory=file_name)
    
    # Проверка наличия шаблона в папке
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Шаблоны")
    my_files_page.right_click_and_select_action(file_name,"Открыть")
    assert my_files_page.find_file_by_name(dotx_name, "dotx") is not None, f"Файл '{dotx_name}.dotx' не найден"
    my_files_page.right_click_and_select_action(dotx_name,"Снять с публикации")
    
    # Удаление шаблона из "Мои файлы"
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(dotx_name,"Переместить в Корзину")

    refresh_and_wait(admin_driver, logger)