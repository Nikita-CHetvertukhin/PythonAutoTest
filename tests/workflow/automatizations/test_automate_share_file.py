import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import USER1_LOGIN, USER2_LOGIN, USER3_LOGIN, USER4_LOGIN, USER5_LOGIN
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
import allure
from utils.get_date import get_timestamp, get_uuid

process_name = f"{get_uuid()}_test_automate_share_file_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.combo
@pytest.mark.parametrize(("setup_create_delete_process", "setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Automatizations_Share.dzwf",
            "publishing": True,
            "unique_check": True
        },
        {
            "file_type": "Новый документ",
            "open_file": True
        },
        {
            "deadline": get_date("today"),
            "task_type" : process_name,
            "task_executor": USER1_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automate_share_file(error_handler, logger, admin_driver, user1_driver, setup_create_delete_process, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет автоматизацию по предоставлению доступа к файлу"""
    process_name, workflows_page, xpath = setup_create_delete_process
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    user1_my_task_page = MyTasksPage(user1_driver, logger)

    logins_and_access1 = [(USER1_LOGIN, "Полный доступ"), (USER2_LOGIN, "Просмотр"), (USER3_LOGIN, "Комментирование"), (USER4_LOGIN, "Рецензирование"), (USER5_LOGIN, "Полный доступ")]
    logins_and_access2 = [(USER1_LOGIN, "Просмотр"), (USER2_LOGIN, "Просмотр"), (USER3_LOGIN, "Комментирование"), (USER4_LOGIN, "Рецензирование"), (USER5_LOGIN, "Полный доступ")]

    logger.info("Проверка автоматизации на предоставление доступа к файлу")
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    
    assert (result := my_files_editor_page.share_access(action="check", logins_and_access=logins_and_access1))is True,f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."

    # Закрываем задачу под исполнителем
    user1_my_task_page.find_click_header_menu("Мои задачи")
    user1_my_task_page.find_click_side_menu("Мои задачи")
    subtasks = [(1, "Sharing_test", "Выход")]
    user1_my_task_page.complete_task(task_name, subtasks)

    # Проверяем доступы под админом после завершения задачи
    refresh_and_wait(admin_driver, logger)
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    assert (result := my_files_editor_page.share_access(action="check", logins_and_access=logins_and_access2))is True,f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access2}."