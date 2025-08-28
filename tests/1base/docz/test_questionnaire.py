import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_editor_page import MyFilesEditorPage
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "file_type": "Новый документ",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_questionnaire(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет появление вкладки Анкета при привязке переменной"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    text = "questionnairetest"
    test = "variable"

    logger.info("Начало проверки создания простого docx")
    # Ввод текста
    my_files_editor_page.send_text_in_doc(text)
    # Создание первое переменной в схеме и привязка к тексту
    my_files_editor_page.open_side_panel_in_doc("Схема")
    my_files_editor_page.create_first_variable(test)
    my_files_editor_page.tie_to_schema(text, test)
    # Проверка, что появилась вкладка "Анкета"
    assert my_files_editor_page.open_side_panel_in_doc("Анкета")
    # Дополнительная проверка наличия перемнной в анкете и дсотупность заполнения
    my_files_editor_page.find_and_send_variable_in_questionnaire("Текст", "variable", "questionnairetest")