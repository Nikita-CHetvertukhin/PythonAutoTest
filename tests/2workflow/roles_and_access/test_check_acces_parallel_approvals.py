import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait
from pages.my_tasks_page import MyTasksPage
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, USER1_LOGIN, USER2_LOGIN, USER3_LOGIN, USER4_LOGIN, USER5_LOGIN
from locators.my_files_editor_locators import MyFilesEditorLocators
import allure

# Сокращенный вариант при условии выноса проверки Смены исполнителя и Дорабокти в отдельные тест-кейсы
logins_and_access_default = [(USER1_LOGIN, "Полный доступ"),(USER2_LOGIN, "Рецензирование"),(USER3_LOGIN, "Комментирование"),(USER4_LOGIN, "Просмотр")]
logins_and_access_final = [(USER1_LOGIN, "Просмотр"),(USER2_LOGIN, "Просмотр"),(USER3_LOGIN, "Просмотр"),(USER4_LOGIN, "Просмотр")]

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
            "task_type" : "Параллельное согласование",
            "executors_massive": logins_and_access_default,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
@allure.epic('Workflow')
@allure.feature('Роли и доступы')
@allure.title('Проверка доступов при параллельном согласовании')
def test_check_acces_parallel_approvals(
    error_handler, logger, admin_driver, user1_driver, user2_driver, user3_driver, user4_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет доступы при параллельном согласовании"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    # Все драйверы УЗ
    user1_my_tasks_page = MyTasksPage(user1_driver, logger)
    user2_my_tasks_page = MyTasksPage(user2_driver, logger)
    user3_my_tasks_page = MyTasksPage(user3_driver, logger)
    user4_my_tasks_page = MyTasksPage(user4_driver, logger)

    logger.info(f"Начало проверки доступов для системного процесса: 'Параллельное согласование'")
    # Проверяем натсройки доступов к файлу после создания задачи
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access_default)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access_default}."
    
    # Закрываем задачу УЗ1
    user1_my_tasks_page.find_click_header_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Мои задачи")
    user1_my_tasks_page.click_if_fa_caret_right(task_name)
    user1_my_tasks_page.complete_task(task_name, [(1, USER1_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ2
    user2_my_tasks_page.find_click_header_menu("Мои задачи")
    user2_my_tasks_page.find_click_side_menu("Мои задачи")
    user2_my_tasks_page.click_if_fa_caret_right(task_name)
    user2_my_tasks_page.complete_task(task_name, [(1, USER2_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ3
    user3_my_tasks_page.find_click_header_menu("Мои задачи")
    user3_my_tasks_page.find_click_side_menu("Мои задачи")
    user3_my_tasks_page.click_if_fa_caret_right(task_name)
    user3_my_tasks_page.complete_task(task_name, [(1, USER3_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ4
    user4_my_tasks_page.find_click_header_menu("Мои задачи")
    user4_my_tasks_page.find_click_side_menu("Мои задачи")
    user4_my_tasks_page.click_if_fa_caret_right(task_name)
    user4_my_tasks_page.complete_task(task_name, [(1, USER4_LOGIN, "Согласовать")])
    
    # Финально проверяем доступы после закрытия задачи
    refresh_and_wait(admin_driver, logger)
    button = xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10)
    time.sleep(1)
    button.click()
    assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access_final)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access_final}."