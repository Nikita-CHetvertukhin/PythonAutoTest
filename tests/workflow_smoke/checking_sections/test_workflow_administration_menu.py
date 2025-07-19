import pytest
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from pages.workflow_administration_page import WorkflowAdministrationPage
from locators.workflow_administration_locators import WorkflowAdministrationLocators

DRIVERS = ["admin_driver", "expert_driver", "user1_driver"]

@pytest.mark.parametrize("driver_fixture_name", DRIVERS)
@exception_handler  # Декоратор, обрабатывающий исключения, чтобы тест не прерывался неожиданно
def test_workflow_administration(request, error_handler, logger, driver_fixture_name):
    """Тест проверяет доступность разедла 'Workflows (адм) - Все задачи (отладка)' и фиксирует ошибки, если они есть."""
    
    logger.info("Начало проверки раздела 'Workflows (адм) - Все задачи (отладка)'")

    # Переопределение драйвера для использования разных из фисктуры
    driver = request.getfixturevalue(driver_fixture_name)
    # Создаем экземпляр страницы задач с переданным драйвером и логгером
    workflow_administration_page = WorkflowAdministrationPage(driver, logger)

    # Переход в раздел "'Workflows (адм) - Все задачи (отладка)'"
    result = workflow_administration_page.find_click_header_menu("Workflow (адм)", "Все задачи (отладка)")
    if driver_fixture_name != "admin_driver":
        if result:
            raise AssertionError(f"Неверный доступ: роль '{driver_fixture_name}' не должна видеть раздел 'Workflow (адм)'")
        else:
            logger.info(f"Ожидаемый отказ в доступе для роли '{driver_fixture_name}'")
            assert True
            return  # Завершаем тест — роль не должна иметь доступ
    else:
        assert result, "Администратору не удалось перейти в раздел 'Все задачи (отладка)'"

    # Проверяем Navigator Listbox со списком задач
    success, details = workflow_administration_page.verify_columns_visibility(WorkflowAdministrationLocators.COLUMN_NAVIGATOR_LISTBOX,WorkflowAdministrationLocators.SCROLLER_NAVIGATION_LISTBOX,
        "check","Задача","isTemplate","isPublished","removed","System","Hidden","isClosed"
    )

    if success:
        logger.info("Проверка видимости колонок прошла успешно.")
    assert success, f"Ошибка проверки видимости колонок: {details}"
