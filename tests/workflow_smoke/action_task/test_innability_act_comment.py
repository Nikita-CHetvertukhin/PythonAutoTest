import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import USER1_LOGIN
from pages.my_tasks_page import MyTasksPage
from locators.my_tasks_locators import MyTasksLocators

@pytest.mark.combo
@pytest.mark.parametrize(
    "setup_create_delete_task",
    [{"task_executor": USER1_LOGIN}],
    indirect=True
)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_innability_act_comment(error_handler, logger, admin_driver, user1_driver, setup_create_delete_task):
    """Тест проверяет невозможнотсь измения/удаления чужого комментария к задаче"""
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_tasks_page_user1 = MyTasksPage(user1_driver, logger)
    xpath_user1 = my_tasks_page_user1.xpath

    logger.info("Начало невозможнотси измения/удаления чужого комментария к задаче")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    my_tasks_page.task_comment_properties(comment_text="test_comment", action="set")

    my_tasks_page_user1.find_click_header_menu("Мои задачи")
    my_tasks_page_user1.find_click_side_menu("Мои задачи")
    time.sleep(1)  # TODO: заменить на ожидание состояния страницы
    my_tasks_page_user1.right_click_and_select_action(task_name, "Открыть")
    my_tasks_page_user1.task_comment_properties(comment_text="test_comment", action="check")
    assert xpath_user1.not_find(MyTasksLocators.MY_TASKS_TASKFORM_COMMENT_EDIT_BUTTON, 
                          timeout=2), "Ошибка: кнопка редактирования комментария к задаче видима для пользователя, который не является автором комментария."
    logger.info(
        "Кнопка редактирования чужого комментария к задаче не найдена")
    assert xpath_user1.not_find(MyTasksLocators.MY_TASKS_TASKFORM_COMMENT_DELETE_BUTTON,
                          timeout=2), "Ошибка: кнопка удаления комментария к задаче видима для пользователя, который не является автором комментария."
    logger.info(
        "Кнопка удаления чужого комментария к задаче не найдена")