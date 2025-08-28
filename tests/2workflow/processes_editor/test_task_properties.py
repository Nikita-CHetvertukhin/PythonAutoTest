import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import USER1_LOGIN
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_task_properties(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет доступность для изменения и сохранение после перезагрузки страницы свойств фигуры 'Задача'"""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки свойств фигуры 'Задача'")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    # Устанавливаем свойства процесса
    workflow_editor_page.role_properties(role_name="test_role",action="create",checkboxes="ON", access_level="Комментирование",users={USER1_LOGIN})
    workflow_editor_page.stages_properties(action="add", name="test_1", number="1")

    # Создаем фигуры и соединяем их
    first_shape = workflow_editor_page.add_shape("Задача") # Создание первой фигуры
    second_shape = workflow_editor_page.add_shape("Выход") # Создание второй фигуры
    workflow_editor_page.drag_element_right(second_shape, offset=500) # Перетаксикваем вторую фигуру вправо
    connection_shape = workflow_editor_page.connect_shapes(first_shape, second_shape) # Коннектим
    
    # Открываем свойства фигуры "Задача" и устанавливаем их
    workflow_editor_page.click_shape(first_shape)
    workflow_editor_page.name_properties("new_name", "set")
    workflow_editor_page.descriptions_properties("new_description", "set")
    workflow_editor_page.term_properties("2m 2d 2w 2h", "set")
    workflow_editor_page.notify_properties("ежедневно, начиная за неделю до срока", "set")
    workflow_editor_page.executor_properties("test_role","set")
    workflow_editor_page.shape_stages_properties("test_1","set")
    workflow_editor_page.observer_properties(action="add", role_name="test_role", users={USER1_LOGIN})
    workflow_editor_page.connections_properties(action="set", target_element="Выход",trans_name="test_trans", result="1")
    workflow_editor_page.automation_start(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    workflow_editor_page.automation_finish(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    time.sleep(1) # Пауза для стабильности (была 2)

    refresh_and_wait(admin_driver, logger)

    workflow_editor_page.click_shape(first_shape)
    assert workflow_editor_page.name_properties("new_name", "check")
    assert workflow_editor_page.descriptions_properties("new_description", "check")
    assert workflow_editor_page.term_properties("76d 2h", "check")
    assert workflow_editor_page.notify_properties("7d;6d;5d;4d;3d;2d;1d", "check")
    assert workflow_editor_page.executor_properties("test_role","check")
    assert workflow_editor_page.shape_stages_properties("test_1","check")
    assert workflow_editor_page.observer_properties(action="check", role_name="test_role", users={USER1_LOGIN})
    assert workflow_editor_page.connections_properties(action="check", target_element="Выход",trans_name="test_trans", result="1")
    assert workflow_editor_page.automation_start(action_type="check", automation_type="DOCZ: Сохранение данных в БД")
    assert workflow_editor_page.automation_finish(action_type="check", automation_type="DOCZ: Сохранение данных в БД")