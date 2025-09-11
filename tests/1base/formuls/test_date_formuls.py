import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
from utils.get_date import get_date, get_timezone_info
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.base_smoke
@pytest.mark.base
@pytest.mark.parametrize("setup_create_delete_file", [{
    "upload_file_name": "AQA_Test_Formuls_Date.dotx",
    "open_file": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_date_formuls(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет работу формул с датой"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    today = get_date("today")
    gmt_format = get_timezone_info()

    logger.info("Начало проверки работы формул с датой")
    my_files_editor_page.open_side_panel_in_doc("Анкета")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Дата", "Исходная дата", "02.04.2024")
    my_files_editor_page.find_and_send_variable_in_questionnaire("Дата", "Другая дата", "03.04.2024")
    # Проверки работы формул
    assert my_files_editor_page.check_content_in_doc("02.04.2024", "1")
    assert my_files_editor_page.check_content_in_doc("03.04.2024", "2")
    assert my_files_editor_page.check_content_in_doc("1", "3")
    assert my_files_editor_page.check_content_in_doc("1", "4")
    assert my_files_editor_page.check_content_in_doc("24", "5")
    assert my_files_editor_page.check_content_in_doc("1 440", "6")
    assert my_files_editor_page.check_content_in_doc("86 400", "7")
    assert my_files_editor_page.check_content_in_doc("04.04.2024", "8")
    assert my_files_editor_page.check_content_in_doc("02.06.2024", "9")
    assert my_files_editor_page.check_content_in_doc("02.04.2026", "10")
    assert my_files_editor_page.check_content_in_doc("Апрель", "11")
    assert my_files_editor_page.check_content_in_doc("Апр", "12")
    assert my_files_editor_page.check_content_in_doc("Вторник", "13")
    assert my_files_editor_page.check_content_in_doc("Вт", "14")
    assert my_files_editor_page.check_content_in_doc("1", "15")
    assert my_files_editor_page.check_content_in_doc("01.04.2024", "16")
    assert my_files_editor_page.check_content_in_doc("true", "17")
    assert my_files_editor_page.check_content_in_doc("0", "18")
    assert my_files_editor_page.check_content_in_doc("2", "19")
    assert my_files_editor_page.check_content_in_doc(f"Mon Apr 01 2024 00:00:00 GMT{gmt_format}", "20", partial_match=True)
    assert my_files_editor_page.check_content_in_doc(f"Tue Apr 30 2024 00:00:00 GMT{gmt_format}", "21", partial_match=True)
    assert my_files_editor_page.check_content_in_doc(f"Mon Apr 01 2024 00:00:00 GMT{gmt_format}", "22", partial_match=True)
    assert my_files_editor_page.check_content_in_doc(f"Mon Jan 01 2024 00:00:00", "23", partial_match=True)
    assert my_files_editor_page.check_content_in_doc("30", "24")
    assert my_files_editor_page.check_content_in_doc(f"2024-04-02T00:00:00", "25", partial_match=True)
    assert my_files_editor_page.check_content_in_doc("01.04.2024", "26")
    assert my_files_editor_page.check_content_in_doc("01.01.2024", "27")
    assert my_files_editor_page.check_content_in_doc("2 024", "28")
    assert my_files_editor_page.check_content_in_doc("02.04.2030", "29")
    assert my_files_editor_page.check_content_in_doc(f"{today}", "30")