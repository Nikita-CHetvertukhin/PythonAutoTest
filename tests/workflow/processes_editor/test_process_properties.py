import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import USER1_LOGIN

@pytest.fixture
def setup_test_process_properties(request, logger, admin_driver):
    """Фикстура для создания и удаления процесса."""
    workflows_page = WorkflowsPage(admin_driver, logger)
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)
    process_name = workflows_page.generate_object_name()

    logger.info("Создание процесса...")
    workflows_page.find_click_header_menu("Рабочие процессы")
    workflows_page.find_click_side_menu("Шаблоны процессов")
    time.sleep(1)  # Ждем, чтобы страница успела загрузиться Потом поправить на ожидание request
    workflows_page.create_process(process_name)

    # Проверяем, что процесс действительно создался
    if not workflows_page.find_process_by_name(process_name):
        logger.error(f"Ошибка: процесс '{process_name}' не был создан!")
        pytest.fail(f"Тест провален. Процесс '{process_name}' не был создан.", pytrace=False)

    def cleanup():
        """Удаление процесса после теста."""
        logger.info(f"Удаление процесса '{process_name}'...")
        time.sleep(2)  # Ждём явно, пока не появятся статусы сохранения
        workflows_page.click_header_logo_button()
        refresh_and_wait(admin_driver, logger)
        workflows_page.find_click_header_menu("Рабочие процессы")
        workflows_page.find_click_side_menu("Шаблоны процессов")
        process_to_delete = workflows_page.find_process_by_name(process_name)
        if process_to_delete:
            workflows_page.right_click_and_select_action(process_name, "Переместить в Корзину")
            logger.info(f"Процесс '{process_name}' перемещен в корзину.")
        else:
            logger.warning(f"Процесс '{process_name}' не найден для удаления.")

    request.addfinalizer(cleanup)  # Гарантированное удаление процесса
    return process_name, workflows_page, workflow_editor_page

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_process_properties(error_handler, logger, admin_driver, setup_test_process_properties):
    """Тест проверяет доступность для изменения и сохранение после перезагрузки страницы свойств процесса"""
    process_name, workflows_page, workflow_editor_page = setup_test_process_properties

    logger.info("Начало проверки свойств процесса")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    workflow_editor_page.name_properties("new_name", "set")
    workflow_editor_page.descriptions_properties("new_description", "set")
    workflow_editor_page.term_properties("2m 2d 2w 2h", "set")
    workflow_editor_page.role_properties(role_name="test_role",action="create",checkboxes="OFF", access_level="Комментирование",users={USER1_LOGIN})
    workflow_editor_page.observer_properties(action="add", role_name="test_role", users={USER1_LOGIN})
    workflow_editor_page.variables_properties(action="add", id="test_id", name="test_name", comment="test_comment", type="String", content="test_content")
    workflow_editor_page.notify_properties("ежедневно, начиная за неделю до срока", "set")
    workflow_editor_page.stages_properties(action="add", name="test_1", number="1")
    workflow_editor_page.automation_start(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    workflow_editor_page.automation_finish(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    time.sleep(2)

    refresh_and_wait(admin_driver, logger)
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    assert workflow_editor_page.name_properties("new_name", "check")
    assert workflow_editor_page.descriptions_properties("new_description", "check")
    assert workflow_editor_page.term_properties("76d 2h", "check")
    assert workflow_editor_page.role_properties(role_name="test_role",action="check",checkboxes=None, access_level="Комментирование [◦◦◦◦◦◦◦]",users={USER1_LOGIN})
    assert workflow_editor_page.observer_properties(action="check", role_name="test_role", users={USER1_LOGIN})
    assert workflow_editor_page.variables_properties(action="check", id="test_id", name="test_name", comment="test_comment", type="String", content="test_content")
    assert workflow_editor_page.notify_properties("7d;6d;5d;4d;3d;2d;1d", "check")
    assert workflow_editor_page.stages_properties(action="check", name="test_1", number="1")
    assert workflow_editor_page.automation_start(action_type="check", automation_type="DOCZ: Сохранение данных в БД")
    assert workflow_editor_page.automation_finish(action_type="check", automation_type="DOCZ: Сохранение данных в БД")

    # P.s. наеврное можно оптимизировать универсальным методом add и check для всех свойств, но пока не стал из-за того что в некоторых методах отличается более одного свойства