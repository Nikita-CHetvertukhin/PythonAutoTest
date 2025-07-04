import pytest
import time
from utils.exception_handler.decorator_error_handler import exception_handler
from pages.workflows_page import WorkflowsPage
from pages.workflow_editor_page import WorkflowEditorPage
from utils.refresh_and_wait import refresh_and_wait
from settings.variables import USER1_LOGIN

@pytest.fixture
def setup_test_task_properties(request, logger, admin_driver):
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
def test_task_properties(error_handler, logger, admin_driver, setup_test_task_properties):
    """Тест проверяет доступность для изменения и сохранение после перезагрузки страницы свойств фигуры 'Задача'"""
    process_name, workflows_page, workflow_editor_page = setup_test_task_properties

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
    time.sleep(2)

    refresh_and_wait(admin_driver, logger)
    time.sleep(2)  # Ждем, пока откроется страница процесса. Использовано явное ожидание т.к. не на что ориентироваться

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


    # P.s. наеврное можно оптимизировать универсальным методом add и check для всех свойств, но пока не стал из-за того что в некоторых методах отличается более одного свойства