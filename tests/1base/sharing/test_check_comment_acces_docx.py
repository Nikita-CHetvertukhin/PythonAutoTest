import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import EXPERT_LOGIN
from utils.licence_checker import is_licence_enabled
from utils.element_searching import XPathFinder
from settings.variables import SHARING_INNER, COLLABORATION
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
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
    "upload_file_name": "AQA_Test_Acces_docx.docx",
    "share_from": EXPERT_LOGIN,
    "share_acces": "Комментирование"
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_check_comment_acces_docx(error_handler, logger, admin_driver, expert_driver, setup_create_delete_file):
    """Тест проверяет уровень доступа 'Комментирование' для docx."""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    xpath_expert = XPathFinder(expert_driver)
    my_files_expert = MyFilesPage(expert_driver, logger)
    my_files_editor_expert = MyFilesEditorPage(expert_driver, logger)
    coloboration_box = is_licence_enabled(COLLABORATION)

    logger.info("Начало проверки уровня доступа 'Комментирование'")
    my_files_expert.click_header_logo_button()
    my_files_expert.find_click_header_menu("Документы")
    my_files_expert.find_click_side_menu("Доступные мне")
    # Проверка действий из ПКМ
    result = my_files_expert.get_action_availability("docx", "Комментирование",coloboration_box)
    my_files_expert.right_click_and_check_acces(file_name, result)
    # Проверка внесений изменений в текст + боковых панелей для абзаца/таблицы/картинки
    my_files_editor_expert.check_acces_in_editor(acces_level="Комментирование", setting_type="Настройки абзаца", text="justParagraph")
    my_files_editor_expert.check_acces_in_editor(acces_level="Комментирование", setting_type="Настройки таблицы", text="justTable")
    my_files_editor_expert.check_acces_in_editor(acces_level="Комментирование", setting_type="Настройки изображения", element_class="drawing")
    # Проверка невозможности создания первой переменной на вкладке "схема"
    my_files_editor_expert.open_side_panel_in_doc("Схема")
    assert not my_files_editor_expert.create_first_variable("test"), "Первая переменная успешно добавлена в docx, несмотря на то, что уровень доступа - Комментирование"
    # Проверка действий на вкладках тулбара
    my_files_editor_expert.check_acces_in_header_section(acces_level="Комментирование", section_name="Конструктор")
    my_files_editor_expert.check_acces_in_header_section(acces_level="Комментирование", section_name="Главная")
    my_files_editor_expert.check_acces_in_header_section(acces_level="Комментирование", section_name="Вставка")
    my_files_editor_expert.check_acces_in_header_section(acces_level="Комментирование", section_name="Макет")
    if coloboration_box:
        my_files_editor_expert.check_acces_in_header_section(acces_level="Комментирование", section_name="Рецензирование")