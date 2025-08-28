import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait
from pages.my_tasks_page import MyTasksPage
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, USER1_LOGIN, USER2_LOGIN, USER3_LOGIN, USER4_LOGIN, USER5_LOGIN
from locators.my_files_editor_locators import MyFilesEditorLocators
import allure

# # Массивный тест-кейс
# # Стандартной набор при создании задачи
# logins_and_access_default = [(USER5_LOGIN, "Полный доступ"),(USER2_LOGIN, "Рецензирование"),(USER3_LOGIN, "Комментирование"),(USER4_LOGIN, "Просмотр")]
# # После смены исполнителя
# logins_and_access1 = [(USER5_LOGIN, "Просмотр"),(USER2_LOGIN, "Рецензирование"),(USER3_LOGIN, "Комментирование"),(USER4_LOGIN, "Просмотр"),(USER1_LOGIN, "Полный доступ")]
# # После выполнения первой задачи
# logins_and_access2 = [(USER5_LOGIN, "Просмотр"),(USER2_LOGIN, "Рецензирование"),(USER3_LOGIN, "Комментирование"),(USER4_LOGIN, "Просмотр"),(USER1_LOGIN, "Просмотр")]
# # После отпарвки на доработку
# logins_and_access3 = [(USER5_LOGIN, "Просмотр"),(USER2_LOGIN, "Просмотр"),(USER3_LOGIN, "Комментирование"),(USER4_LOGIN, "Просмотр"),(USER1_LOGIN, "Просмотр")]
# # После выполнения задачи
# logins_and_access_final = [(USER5_LOGIN, "Просмотр"),(USER2_LOGIN, "Просмотр"),(USER3_LOGIN, "Просмотр"),(USER4_LOGIN, "Просмотр"),(USER1_LOGIN, "Просмотр")]

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
    
    # # Меняем исполнителя для первой задачи и проверяем доступы
    # my_tasks_page.find_click_header_menu("Мои задачи")
    # my_tasks_page.find_click_side_menu("Мои задачи")
    # my_tasks_page.open_subtask(task_name, subtask_massive=[(1, USER5_LOGIN)])
    # my_tasks_page.task_executor_properties(executor_login=USER1_LOGIN, action="set")
    # my_tasks_page.find_click_header_menu("Документы")
    # my_tasks_page.find_click_side_menu("Мои файлы")
    # my_files_page.right_click_and_select_action(file_name, "Открыть")
    # time.sleep(1)  # TODO Заменить на динамическое ожидание
    # xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    # assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access1)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."

    # # Авторизовываемся под новым исполнителем и выполняем задачу
    # user1_my_tasks_page.find_click_header_menu("Мои задачи")
    # user1_my_tasks_page.find_click_side_menu("Мои задачи")
    # user1_my_tasks_page.complete_task(task_name, [(1, USER5_LOGIN, "Согласовать")])
    # # Проверяем доступы после выполнения задачи
    # refresh_and_wait(admin_driver, logger)
    # xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    # assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access2)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access2}."

    # # Авторизовываемся под вторым исполнителем и отправляем на доработку
    # user2_my_tasks_page.find_click_header_menu("Мои задачи")
    # user2_my_tasks_page.find_click_side_menu("Мои задачи")
    # user2_my_tasks_page.complete_task(task_name, subtask_massive=[(1, USER2_LOGIN, "Отправить на доработку")], waiting=False)
    # user2_my_tasks_page.add_required_comment(text_comment=f"sending_to_rework_from_{USER2_LOGIN}")
    # # Проверяем доступы после отправки на доработку
    # refresh_and_wait(admin_driver, logger)
    # xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    # assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access3)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access3}."

    # # Выполняем доработку и проверяем доступы
    # my_tasks_page.find_click_header_menu("Мои задачи")
    # my_tasks_page.find_click_side_menu("Мои задачи")
    # my_tasks_page.complete_task(task_name, subtask_massive=[(5, "Доработка", "Согласовать")])
    # my_tasks_page.find_click_header_menu("Документы")
    # my_tasks_page.find_click_side_menu("Мои файлы")
    # my_files_page.right_click_and_select_action(file_name, "Открыть")
    # time.sleep(1)  # TODO Заменить на динамическое ожидание
    # xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    # assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access1)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access1}."

    # Закрываем задачу УЗ1
    user1_my_tasks_page.find_click_header_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Мои задачи")
    user1_my_tasks_page.complete_task(task_name, [(1, USER1_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ2
    user2_my_tasks_page.find_click_header_menu("Мои задачи")
    user2_my_tasks_page.find_click_side_menu("Мои задачи")
    user2_my_tasks_page.complete_task(task_name, [(1, USER2_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ3
    user3_my_tasks_page.find_click_header_menu("Мои задачи")
    user3_my_tasks_page.find_click_side_menu("Мои задачи")
    user3_my_tasks_page.complete_task(task_name, [(1, USER3_LOGIN, "Согласовать")])
    # Закрываем задачу УЗ4
    user4_my_tasks_page.find_click_header_menu("Мои задачи")
    user4_my_tasks_page.find_click_side_menu("Мои задачи")
    user4_my_tasks_page.complete_task(task_name, [(1, USER4_LOGIN, "Согласовать")])
    
    # Финально проверяем доступы после закрытия задачи
    refresh_and_wait(admin_driver, logger)
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=10).click()
    assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access_final)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access_final}."