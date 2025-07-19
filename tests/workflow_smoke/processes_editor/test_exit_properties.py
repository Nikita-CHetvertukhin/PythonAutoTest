import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage
from utils.refresh_and_wait import refresh_and_wait

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_exit_properties(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет доступность для изменения и сохранение после перезагрузки страницы свойств фигуры 'Выход'"""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки свойств фигуры 'Выход'")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    # Создаем фигуры и соединяем их
    first_shape = workflow_editor_page.add_shape("Вход") # Создание первой фигуры
    second_shape = workflow_editor_page.add_shape("Выход") # Создание второй фигуры
    workflow_editor_page.drag_element_right(second_shape, offset=500) # Перетаксикваем вторую фигуру вправо
    connection_shape = workflow_editor_page.connect_shapes(first_shape, second_shape) # Коннектим
    
    # Открываем свойства фигуры "Выход" и устанавливаем их
    workflow_editor_page.click_shape(second_shape)
    workflow_editor_page.name_properties("new_name", "set")
    workflow_editor_page.descriptions_properties("new_description", "set")
    workflow_editor_page.shape_exit_result_properties("set", "fail")
    workflow_editor_page.automation_start(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    workflow_editor_page.automation_finish(action_type="add", automation_type="DOCZ: Сохранение данных в БД")
    time.sleep(2)

    refresh_and_wait(admin_driver, logger)
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    workflow_editor_page.click_shape(second_shape)
    assert workflow_editor_page.name_properties("new_name", "check")
    assert workflow_editor_page.descriptions_properties("new_description", "check")
    assert workflow_editor_page.shape_exit_result_properties("check", "fail")
    assert workflow_editor_page.automation_start(action_type="check", automation_type="DOCZ: Сохранение данных в БД")
    assert workflow_editor_page.automation_finish(action_type="check", automation_type="DOCZ: Сохранение данных в БД")

    # P.s. наеврное можно оптимизировать универсальным методом add и check для всех свойств, но пока не стал из-за того что в некоторых методах отличается более одного свойства