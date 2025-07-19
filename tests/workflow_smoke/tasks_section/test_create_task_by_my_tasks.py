import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN

@pytest.mark.parametrize(
    "setup_create_delete_task",[{
    "deadline": get_date("today"),
    "description": "test_description",
    "task_type": "Простая задача",
    "task_executor": ADMIN_LOGIN
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_create_task_by_my_tasks(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет создание задачи через 'Мои задачи'"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Проверка созданной задачи через 'Мои задачи'")
    goal_task = my_tasks_page.find_task_by_name(task_name)
    goal_task.click()
    assert my_tasks_page.task_name_properties(task_name, action="check"), f"Ошибка: Название задачи '{task_name}' не совпадает с найденным."
    assert my_tasks_page.task_description_properties("test_description", action="check"), "Ошибка: Описание задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_deadline_properties(get_date("today"), action="check"), "Ошибка: Дедлайн задачи не совпадает с ожидаемым."
    assert my_tasks_page.task_executor_properties(ADMIN_LOGIN, action="check"), f"Ошибка: Исполнитель задачи не совпадает с ожидаемым '{ADMIN_LOGIN}'."
