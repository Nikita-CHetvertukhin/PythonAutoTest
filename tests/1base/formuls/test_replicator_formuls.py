import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Replicator.dotx",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
@allure.epic('Коробка')
@allure.feature('Формулы')
@allure.title('Проверка формул с мультипликатором')
def test_replicator_formuls(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет работу формул с мультипликатором"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)

    logger.info("Начало проверки работы формул с мультипликатором")
    my_files_editor_page.open_side_panel_in_doc("Анкета")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Условие", "Открыть мультипликатор для внесения изменений")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 1",
                                                                 replica_name="Мультипликатор 1 1", replica_action="Добавить")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 1", content="Бананы",
                                                                 in_replicator=True, replica_name="Мультипликатор 1 1", variable_in_replica_type="Текст",
                                                                 variable_in_replica_name="Продукт")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 1", content=100,
                                                                 in_replicator=True, replica_name="Мультипликатор 1 1", variable_in_replica_type="Число",
                                                                 variable_in_replica_name="Стоимость")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 1", content="Яблоки",
                                                                 in_replicator=True, replica_name="Мультипликатор 1 2", variable_in_replica_type="Текст",
                                                                 variable_in_replica_name="Продукт")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 1", content=200,
                                                                 in_replicator=True, replica_name="Мультипликатор 1 2", variable_in_replica_type="Число",
                                                                 variable_in_replica_name="Стоимость")
    # Проверки работы формул
    assert my_files_editor_page.check_content_in_doc("Бананы", "4")
    assert my_files_editor_page.check_content_in_doc("100,00 руб.", "5")
    assert my_files_editor_page.check_content_in_doc("Яблоки", "6")
    assert my_files_editor_page.check_content_in_doc("200,00 руб.", "7")
    assert my_files_editor_page.check_content_in_doc("2", "9")
    assert my_files_editor_page.check_content_in_doc("100,00 руб.", "11")
    assert my_files_editor_page.check_content_in_doc("200,00 руб.", "13")
    assert my_files_editor_page.check_content_in_doc("300,00 руб.", "15")
    assert my_files_editor_page.check_content_in_doc("20 000,00 руб.", "17")
    assert my_files_editor_page.check_content_in_doc("150,00 руб.", "19")
    assert my_files_editor_page.check_content_in_doc("true", "21")
    assert my_files_editor_page.check_content_in_doc("Содержится число 100!", "23")
    assert my_files_editor_page.check_content_in_doc("Нет true в переменной мультипликатора", "25")
    
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 2",
                                                                replica_name="Мультипликатор 2 1", replica_action="Добавить")
    my_files_editor_page.find_and_send_variable_in_questionnaire(variable_type="Мультипликатор", variable_name="Мультипликатор 2",
                                                                in_replicator=True, replica_name="Мультипликатор 2 2", variable_in_replica_type="Условие",
                                                                variable_in_replica_name="Условие")

    assert my_files_editor_page.check_content_in_doc("Есть true в переменной мультипликатора", "25")