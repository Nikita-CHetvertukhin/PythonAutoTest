import time
import pytest
from utils.exception_handler.decorator_error_handler import exception_handler
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_8_17_adding_comment_task(error_handler, logger, admin_driver, setup_create_delete_task):
    """Тест проверяет возможность добавления комментария к задаче"""
    task_name, my_tasks_page, xpath = setup_create_delete_task

    logger.info("Начало проверки добавления комментария")
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    my_tasks_page.task_comment_properties(comment_text="test_comment", action="set")

    refresh_and_wait(admin_driver, logger)

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1)  # TODO: заменить на ожидание состояния страницы
    my_tasks_page.right_click_and_select_action(task_name, "Открыть")
    assert my_tasks_page.task_comment_properties(
        comment_text="test_comment", action="check"), "Комментарий к задаче не совпадает."