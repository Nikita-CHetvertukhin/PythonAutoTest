import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, SHARE_DRIVES
from utils.licence_checker import is_licence_enabled
import allure
from utils.get_date import get_timestamp, get_uuid

drive_name = f"{get_uuid()}_transform_docx_drives_drive_{get_timestamp()}"
process_name = f"{get_uuid()}_transform_docx_drives_process_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.skipif(
    not is_licence_enabled(SHARE_DRIVES),
    reason=f"Лицензия '{SHARE_DRIVES}' отключена — тест пропущен"
)
@pytest.mark.parametrize(("setup_create_delete_drive", "setup_create_delete_process","setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "drive_name": drive_name,
            "unique_check": True
        },
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Automatizations_DOCZ_to_DOCX_drives.dzwf",
            "shape_name" : "Задача",
            "type_auto": "finish",
            "type_section": "Общие диски",
            "name_catalog": drive_name,
            "publishing_to": [ADMIN_LOGIN],
            "unique_check": True
        },
        {
            "upload_file_name": "AQA_ID1.docz",
            "open_file": True
        },
        {
            "task_type" : process_name,
            "task_executor": ADMIN_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automate_transform_docx_drives(request, error_handler, logger, admin_driver, setup_create_delete_drive, setup_create_delete_process, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет работу автоматизации по конвертации анкеты в docx в папку в разделе 'Общие диски'"""
    drive_name, my_files_page, xpath = setup_create_delete_drive
    process_name, workflows_page, xpath = setup_create_delete_process
    file_name, my_files_page, xpath  = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки автоматизации по конвертации docz в docx в папку в разделе 'Общие диски'")
    # Выполняем задачу
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.complete_task(task_name, subtask_massive=[(1, "Задача", "Выход")])

    #проверяем создание папки и преобразование анкеты в docx
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Общие диски")
    my_files_page.right_click_and_select_action(drive_name, "Открыть")
    assert my_files_page.find_file_by_name("AQA_test_automate_transform_from_docz_to_docx_drives"), f"ошибка: папка 'aqa_test_automate_transform_from_docz_to_docx_my_files' не найден в общем диске."
    my_files_page.right_click_and_select_action("AQA_test_automate_transform_from_docz_to_docx_drives", "Открыть")
    assert my_files_page.find_file_by_name(file_name,"docx"), f"ошибка: файл '{file_name}' не найден в папке 'AQA_test_automate_transform_from_docz_to_docx_drives'."