import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait
from pages.my_tasks_page import MyTasksPage
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, USER1_LOGIN, USER2_LOGIN
from locators.my_files_editor_locators import MyFilesEditorLocators
import allure

logins_massive = [(USER2_LOGIN, "Полный доступ")]

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.combo
@pytest.mark.parametrize(
    ("setup_create_delete_file", "setup_create_delete_task"),
    [
        (
            {
                "upload_file_name": "AQA_ID1.docz",
                "open_file": True
            },
            {
                "task_type": "Последовательное согласование",
                "executors_massive": logins_massive,
                "from_file": True
            }
        ),
        (
            {
                "upload_file_name": "AQA_ID1.docz",
                "open_file": True
            },
            {
                "task_type": "Параллельное согласование",
                "executors_massive": logins_massive,
                "from_file": True
            }
        )
    ],
    indirect=True
)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_check_observer_system_approvals(error_handler, logger, admin_driver, user1_driver, user2_driver, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет доступы наблюдателя в одном из системныхз маршуртов согалсования"""
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    # Все драйверы
    user1_my_tasks_page = MyTasksPage(user1_driver, logger)
    user2_my_tasks_page = MyTasksPage(user2_driver, logger)
    
    logger.info(f"Начало проверки доступов наблюдателя для системного маршрута согласования Параллельное или Последовательное'")
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    my_files_page.share_access(action="check", logins_and_access=logins_massive)
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    my_tasks_page.open_subtask(task_name, subtask_massive=[(1, USER2_LOGIN)])
    my_tasks_page.task_oberver_properties(USER1_LOGIN)
    # Проверяем доступ к докмуенту для наблюдателя
    my_tasks_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Мои файлы")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    xpath.find_clickable(MyFilesEditorLocators.ACCESS_BUTTON, timeout=3).click()
    logins_and_access = [(USER2_LOGIN, "Полный доступ"),(USER1_LOGIN, "Просмотр")]
    assert (result := my_files_page.share_access(action="check", logins_and_access=logins_and_access)) is True, f"Ошибка: Доступы {result[1]} не совпадают с ожидаемыми {logins_and_access}."

    # Проверяем доступ к полям задачи для наблюдателя
    user1_my_tasks_page.find_click_header_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Отслеживаемые")
    time.sleep(3) # TODO Разобраться что блокирует открытие подзадачи без ожидания. Мне кажется даже при выключенных уведомлениях появляется какой-то фрейм на всю страницу не видимый для юзера, который сбивает селениум
    user1_my_tasks_page.open_subtask(task_name, subtask_massive=[(1, USER2_LOGIN)])
    assert user1_my_tasks_page.check_access_to_task_fields(fields_massive=[]), "Ошибка в доступе к полям задачи для наблюдателя."

    # Выполняем задачу поди исполнителем и проверяем отсутствие задачи в разделе "Отслеживаемые" у Наблюдателя
    user2_my_tasks_page.find_click_header_menu("Мои задачи")
    user2_my_tasks_page.find_click_side_menu("Мои задачи")
    user2_my_tasks_page.complete_task(task_name, [(1, USER2_LOGIN, "Согласовать")])
    user1_my_tasks_page.click_header_logo_button()
    user1_my_tasks_page.find_click_header_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Мои задачи")
    user1_my_tasks_page.find_click_side_menu("Отслеживаемые")
    time.sleep(3) # TODO Разобраться что блокирует открытие подзадачи без ожидания. Мне кажется даже при выключенных уведомлениях появляется какой-то фрейм на всю страницу не видимый для юзера, который сбивает селениум
    assert not user1_my_tasks_page.find_file_by_name(task_name), f"Задача {task_name} не пропала из раздела отслеживаемые у наблюдателя после закрытия"