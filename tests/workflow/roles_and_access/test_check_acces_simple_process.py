import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from settings.variables import USER1_LOGIN, USER2_LOGIN
from utils.refresh_and_wait import refresh_and_wait
from pages.my_files_editor_page import MyFilesEditorPage
from locators.my_files_editor_locators import MyFilesEditorLocators
from locators.my_tasks_locators import MyTasksLocators
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.combo
@pytest.mark.parametrize(("setup_create_delete_file", "setup_create_delete_task"), 
    [(
        {
            "upload_file_name": "AQA_ID1.docz",
            "open_file": True
        },
        {
            "task_type": "Простой процесс",
            "task_executor": USER2_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
def test_check_acces_simple_process(error_handler, logger, admin_driver, user1_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет изменение доступов к документу в зависимости от смены исполинтеля, завершении задачи для 'Простая задача'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    user1_my_task_page = MyTasksPage(user1_driver, logger)
    my_files_editor_page = MyFilesEditorPage(admin_driver, logger)
    logins_and_access1 = [(USER2_LOGIN, "Полный доступ")]
    logins_and_access2 = [(USER2_LOGIN, "Просмотр"), (USER1_LOGIN, "Полный доступ")]
    logins_and_access3 = [(USER1_LOGIN, "Просмотр"), (USER2_LOGIN, "Просмотр")]
    
    logger.info("Проверка изменения доступов к документу в зависимости от смены исполнителя, завершении задачи для 'Простая задача'")
    # Проверяем права исполнителя после создания задачи
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    assert (result := my_files_editor_page.share_access(action="check", logins_and_access=logins_and_access1))is True,f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."
    
    # Смена исполнителя задачи и проверка доступов для нового/старого исполнителя
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.open_subtask(task_name, subtask_massive=[(1, "Задача")])
    my_tasks_page.task_executor_properties(executor_login=USER1_LOGIN, action="set")
    my_tasks_page.find_click_header_menu("Документы")
    my_tasks_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    time.sleep(1) # TODO Заменить на динамическое ожидание
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    assert (result := my_files_editor_page.share_access(action="check", logins_and_access=logins_and_access2))is True,f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."

    # Завершаем задачу под новым исполнителем
    user1_my_task_page.find_click_header_menu("Мои задачи")
    user1_my_task_page.find_click_side_menu("Мои задачи")
    user1_my_task_page.complete_task(task_name=task_name, subtask_massive=[(1, "Задача", "Выполнить")])

    # Финально проверяем доступы после завершения задачи
    refresh_and_wait(admin_driver, logger)
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    assert (result := my_files_editor_page.share_access(action="check", logins_and_access=logins_and_access3))is True,f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."