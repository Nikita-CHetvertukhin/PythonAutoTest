import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.get_date import get_date
from settings.variables import USER1_LOGIN
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.combo
@pytest.mark.parametrize("setup_create_delete_task",[{
    "deadline": get_date("today"),
    "task_type": "Последовательное согласование",
    "task_executor": USER1_LOGIN,
    "skip_cleanup": True
}], indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_approval_task_after_rework(error_handler, logger, admin_driver, user1_driver, setup_create_delete_task):
    """Тест проверяет возможность выполнения задачи после отправки на доработку (на 2 исполнителях)"""
    task_name, my_tasks_page, xpath = setup_create_delete_task
    user1_my_task_page = MyTasksPage(user1_driver, logger)

    logger.info("Проверка возможности выполнения задачи после отправки на доработку (на 2 исполнителях)")
    # Отправляем на доработку под УЗ исполнителя
    user1_my_task_page.find_click_header_menu("Мои задачи")
    user1_my_task_page.find_click_side_menu("Мои задачи")
    subtasks = [(1, USER1_LOGIN, "Отправить на доработку")]
    user1_my_task_page.complete_task(task_name, subtasks, waiting=False)
    user1_my_task_page.add_required_comment(text_comment=f"{USER1_LOGIN}_test_required_comment")

    # Дорабатываем под УЗ автора
    refresh_and_wait(admin_driver, logger) # Так как отключены вебсокеты , обновляем страницу
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    subtasks = [(2, "Доработка", "Согласовать")]
    my_tasks_page.complete_task(task_name, subtasks)

    # Возвращаемся на УЗ исполнителя и согласовываем задачу
    refresh_and_wait(user1_driver, logger) # Так как отключены вебсокеты , обновляем страницу
    user1_my_task_page.find_click_header_menu("Мои задачи")
    user1_my_task_page.find_click_side_menu("Мои задачи")
    subtasks = [(1, USER1_LOGIN, "Согласовать")]
    user1_my_task_page.complete_task(task_name, subtasks)

    # Возвращаемся на УЗ автора и проверяем, что задача закрыта
    refresh_and_wait(admin_driver, logger)
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Закрытые")
    assert my_tasks_page.find_file_by_name(task_name), f"Ошибка: Задача '{task_name}' не найдена в разделе 'Закрытые'"
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_comment_properties(comment_text=f"{USER1_LOGIN}_test_required_comment", action="check"), "Обязательный комментарий не найден."