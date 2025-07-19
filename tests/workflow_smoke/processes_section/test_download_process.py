import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage
from utils.download_manager import DownloadManager

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_download_process(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет возможность открытия нового процесса через контекстное меню или двойным ЛКМ."""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    download_manager = DownloadManager()

    logger.info("Начало проверки скачивания процесса")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждём явно, пока не появятся статусы сохранения
    workflow_editor_page.action_from_document("Скачать")

    assert download_manager.verify_downloaded_file(f"{process_name}.dzwf"), f"Ошибка: файл '{process_name}.dzwf' не был загружен!"
    logger.info(f"Файл '{process_name}.dzwf' успешно загружен!")