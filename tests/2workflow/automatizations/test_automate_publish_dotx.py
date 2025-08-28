import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.refresh_and_wait import refresh_and_wait
from pages.my_files_page import MyFilesPage
from settings.variables import ADMIN_LOGIN
from utils.get_date import get_date
import allure
from utils.get_date import get_timestamp, get_uuid

process_name = f"{get_uuid()}_test_automate_publish_dotx_{get_timestamp()}"

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.parametrize(("setup_create_delete_process", "setup_create_delete_file", "setup_create_delete_task"),
    [(
        {
            "process_name": process_name,
            "upload_file_name": "AQA_Automatizations_Publish.dzwf",
            "publishing_to": [ADMIN_LOGIN],
            "unique_check": True
        },
        {
            "file_type": "Интерактивный шаблон",
            "open_file": True
        },
        {
            "deadline": get_date("today"),
            "task_type" : process_name,
            "task_executor": ADMIN_LOGIN,
            "from_file": True
        }
    )],
    indirect=True)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automate_publish_dotx(error_handler, logger, admin_driver, setup_create_delete_process, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет работу автоматизации по публикации шаблона (также снимаем с публикации в конце)"""
    process_name, workflows_page, xpath = setup_create_delete_process
    file_name, my_files_page, xpath = setup_create_delete_file
    task_name, my_tasks_page, xpath = setup_create_delete_task
    my_tasks_page = MyTasksPage(admin_driver, logger)

    logger.info("Начало проверки автоматизации по публикации шаблона")

    # Выполнение задачи
    my_tasks_page.find_click_header_menu("Мои задачи")
    my_tasks_page.find_click_side_menu("Мои задачи")
    subtasks = [(1, "Задача", "Выход")]
    my_tasks_page.complete_task(task_name, subtasks)

    # Проверка публикации + снятие с публикации
    my_files_page.find_click_header_menu("Документы")
    my_files_page.find_click_side_menu("Шаблоны")
    assert my_files_page.find_file_by_name(file_name), f"Ошибка: Шаблон '{file_name}' не найден в разделе 'Шаблоны'."
    assert my_files_page.right_click_and_select_action(object_name=f"{file_name}", action_name="Снять с публикации"), f"Ошибка: Не удалось снять с публикации шаблон '{file_name}'."