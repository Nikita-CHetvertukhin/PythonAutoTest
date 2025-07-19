import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.parametrize(
    "setup_create_delete_file",[{
    "file_type": "Новый документ"
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_task_by_my_tasks(error_handler, logger, admin_driver, setup_create_delete_file):
    """Тест проверяет создание задачи через 'Документ'"""
    file_name, my_files_page, xpath = setup_create_delete_file
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Проверка созданной задачи через 'Мои задачи'")
    my_files_page.right_click_and_select_action(file_name, "Открыть")
    time.sleep(1) # Заменить на динамическое ожидание в документе
    my_tasks_page.create_task(task_name=file_name,task_description="test_description", task_type="Простая задача", deadline=get_date("today"),executor=ADMIN_LOGIN, from_file=True)
    time.sleep(1) # Заменить на динамическое ожидание в документе
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    goal_task = my_tasks_page.find_task_by_name(file_name)
    goal_task.click()
    time.sleep(1)  # Заменить на динамическое ожидание пояаления задачи
    assert my_tasks_page.task_name_properties(file_name, action="check"), f"Ошибка: Название задачи '{file_name}' не совпадает с найденным."
    assert my_tasks_page.task_description_properties("test_description", action="check"), "Ошибка: Описание задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_deadline_properties(get_date("today"), action="check"), "Ошибка: Дедлайн задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_executor_properties(ADMIN_LOGIN, action="check"), f"Ошибка: Исполнитель задачи не совпадает с ожидаемым '{ADMIN_LOGIN}'."
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_DELETE_BUTTON, timeout=3).click()
    logger.info("Тест выполнен. Задача успешно удалена через кнопку 'Удалить' в taskform")