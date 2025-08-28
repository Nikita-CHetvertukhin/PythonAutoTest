import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from settings.variables import ADMIN_LOGIN
import allure
from utils.get_date import get_timestamp, get_uuid

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx",
    "publishing_from": [f"{ADMIN_LOGIN}"]
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_docz_from_published_dotx(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет создание анкеты из опубликованного шаблона"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    questionnaire_name = f'test_create_docz_from_published_dotx_{get_uuid()}_{get_timestamp()}'

    logger.info("Начало проверки создания анкеты из опубликованного шаблона")
    # Создание анкеты
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Шаблоны")
    my_files_page.right_click_and_select_action(file_name, "Создать анкету")
    my_files_page.create_docz_from_dotx_section(questionnaire_name)
    my_files_editor_page.waiting_status_after("open")
    # Проверка наличия анкеты в файловой системе
    my_files_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    # Финальная проверка присутствия файла в системе и корректного формата
    assert my_files_page.find_file_by_name(questionnaire_name, "docz") is not None, f"Файл '{questionnaire_name}.docz' не найден"
    my_files_page.right_click_and_select_action(questionnaire_name, "Переместить в Корзину")