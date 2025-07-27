import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait
from pages.my_files_page import MyFilesPage
from pages.my_files_editor_page import MyFilesEditorPage
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from settings.variables import ADMIN_LOGIN
import allure
from utils.get_date import get_timestamp

folder_name = f"AQA_FOLDER_DOCZ_DOCX_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_file", "setup_create_delete_process"),
    [(
        {
            "file_name": folder_name,
            "file_type": "Новую папку",
            "unique_check": True
        },
        {
            "upload_file_name": "AQA_Automatizations_DOCZ_to_DOCX_myfiles.dzwf",
            "shape_name" : "Задача",
            "type_auto": "finish",
            "type_section": "Мои файлы",
            "name_catalog": folder_name,
            "publishing": True
        },
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automate_transform_docx_myfiles(error_handler, logger, admin_driver,setup_create_delete_file, setup_create_delete_process):
    """Тест проверяет работу автоматизации по конвертации анкеты в docx в папку в разделе 'Мои файлы'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    process_name, workflows_page, xpath = setup_create_delete_process
    my_tasks_page = MyTasksPage(admin_driver, logger)
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    # Дополнительно загружаем анкету в раздел "Мои файлы"
    docz_name = my_files_page.upload_file(upload_file_name="AQA_ID1.docz", new_name=f'docz_{process_name}')

    logger.info("Начало проверки автоматизации по конвертации docz в docx в папку в разделе 'Мои файлы'")
    # Создаем задачу из анкеты
    my_tasks_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(docz_name, "Открыть")
    time.sleep(2)  # TODO заменить на данимаческое ожидание
    my_tasks_page.create_task(task_name=f"task_{process_name}", task_type=process_name, executor=ADMIN_LOGIN, from_file=True)
    
    # Выполняем задачу
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.complete_task(f"task_{process_name}", subtask_massive=[(1, "Задача", "Выход")])

    # Проверяем создание папки и преобразование анкеты в docx
    my_tasks_page.click_header_logo_button()
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    assert my_files_page.find_file_by_name("AQA_test_automate_transform_from_docz_to_docx_my_files"), f"Ошибка: Папка 'AQA_test_automate_transform_from_docz_to_docx_my_files' не найдена в папке '{file_name}'."
    my_files_page.right_click_and_select_action("AQA_test_automate_transform_from_docz_to_docx_my_files", "Открыть")
    assert my_files_page.find_file_by_name(docz_name,"docx"), f"Ошибка: Файл '{file_name}' не найден в папке 'AQA_test_automate_transform_from_docz_to_docx_my_files'."

    # Чистим файлы и папку за собой
    try:
        workflows_page.click_header_logo_button()
        my_files_page.right_click_and_select_action(docz_name, "Переместить в Корзину")
    except Exception as e:
        error_handler.handle_exception(MinorIssue(f"Ошибка при удалении файлов: {e}."), critical=False)
        logger.warning(f"Ошибка при удалении файлов (но тест пройден успешно): {e}.")