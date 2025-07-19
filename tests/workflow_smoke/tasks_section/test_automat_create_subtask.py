import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.parametrize("setup_create_delete_process", [{
    "upload_file_name": "AQA_Automatizations_Create_subtask.dzwf",
    "publishing": True
}], indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automat_create_subtask(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет работу автоматизации по созданию подзадачи"""
    process_name, workflows_page, xpath = setup_create_delete_process
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Начало проверки автоматизации по созданию подзадачи")
    task_name = f"task_{process_name}"
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    time.sleep(1) # Ждем, чтобы страница успела загрузиться. Потом поправить на ожидание request
    my_tasks_page.create_task(task_name=task_name, task_type="AQA_Automatizations_Create_subtask")
    # Ждем, чтобы страница успела загрузиться. Потом поправить на ожидание request
    subtasks = [(2, "Созданная подзадача", "Выполнить"),(1, "Основная задача", "Выход")]
    my_tasks_page.complete_task(task_name, subtasks)

    refresh_and_wait(admin_driver, logger)
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    assert not my_tasks_page.find_task_by_name(task_name), f"Ошибка: Задача '{task_name}' не исчезла после выполнения."
    logger.info("Автоматизация по созданию подзадачи успешно выполнена. Задача исчезла после выполнения и не найдена в системе")