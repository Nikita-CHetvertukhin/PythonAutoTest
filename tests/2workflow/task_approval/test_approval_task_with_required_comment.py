import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import ADMIN_LOGIN
from locators.my_tasks_locators import MyTasksLocators
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize("setup_create_delete_task",[{
    "deadline": get_date("today"),
    "task_type": "Параллельное согласование",
    "task_executor": ADMIN_LOGIN
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_approval_task_with_required_comment(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет наличие обязательного комменатрия"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Проверка наличия обязательного комментария")
    # Проверяем отмену обязательного комментария
    subtasks = [(1, ADMIN_LOGIN, "Отправить на доработку")]
    my_tasks_page.complete_task(task_name, subtasks, waiting=False)
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_REQUIRED_COMMENT_CANCEL_BUTTON, timeout=3).click()
    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
    # Проверяем окно обязательного комменатрия и его сохранение
    subtasks = [(1, ADMIN_LOGIN, "Отклонить")]
    my_tasks_page.complete_task(task_name, subtasks, waiting=False)
    my_tasks_page.add_required_comment(text_comment="test_required_comment")
    my_tasks_page.close_all_windows()
    my_tasks_page.find_click_side_menu("Закрытые")
    assert my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не найдена в разделе 'Закрытые'"
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_comment_properties(comment_text="test_required_comment", action="check"), "Обязательный комментарий не найден."