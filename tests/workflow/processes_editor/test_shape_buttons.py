import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflow_editor_page import WorkflowEditorPage
import allure

@allure.severity(allure.severity_level.CRITICAL) # TRIVIAL, MINOR, NORMAL, CRITICAL, BLOCKER
@pytest.mark.workflow_smoke
@pytest.mark.workflow
@exception_handler  # Декоратор обрабатывает исключения и делает скриншот
def test_shape_buttons(error_handler, logger, admin_driver, setup_create_delete_process):
    """Тест проверяет создание, перемещение и соединение фигур в редактоер Workflow."""
    process_name, workflows_page, xpath = setup_create_delete_process
    workflow_editor_page = WorkflowEditorPage(admin_driver, logger)

    logger.info("Начало проверки фигур WF в редакторе")
    workflows_page.right_click_and_select_action(process_name, "Открыть")
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

    # Массив фигур для проверки
    shape_names = ["Вход", "Выход", "Задача", "Условие", "Разветвление", "Слияние"]

    #Цикл проверяет возможность создания каждой из фигур и установления связи между ними каждая фигура выступает в роли связеобразующей
    for primary_shape_name in shape_names:
        if primary_shape_name == "Выход":
            continue  # "Выход" не может быть первым

        primary_shape = workflow_editor_page.add_shape(primary_shape_name) # Создание первой фигуры

        for secondary_shape_name in shape_names:

            secondary_shape = workflow_editor_page.add_shape(secondary_shape_name) # Создание второй фигуры и сохранение её model_id
            workflow_editor_page.drag_element_right(secondary_shape, offset=500) # Поиск и drag&drop второй фигуры по model_id
            connection_shape = workflow_editor_page.connect_shapes(primary_shape, secondary_shape) # Коннект первой и второй фигур
            workflow_editor_page.delete_shape(secondary_shape) # Удаление второй фигуры

        workflow_editor_page.delete_shape(primary_shape) # Удаление первой фигуры