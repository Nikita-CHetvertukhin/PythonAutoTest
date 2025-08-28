import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.my_tasks_page import MyTasksPage
from utils.exception_handler.decorator_error_handler import exception_handler
from settings.variables import ADMIN_LOGIN, URL
import allure
from utils.get_date import get_timestamp

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@pytest.mark.skipif(
    "localhost" not in URL and "docker.internal" not in URL,
    reason="Тест запускается только локально. Без риска для данных на тестовых/клиентских сборках"
)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_automate_save_database(request, error_handler, logger, admin_driver, setup_create_delete_drive, setup_create_delete_process, setup_create_delete_file, setup_create_delete_task):
    """Тест проверяет работу автоматизации по сохранению данных в БД (только для локального теста)"""
    assert False, "Напишу, когда буду заниматься коробкой"