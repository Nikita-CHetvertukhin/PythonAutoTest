from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue
from pages.workflow_administration_page import WorkflowAdministrationPage
from locators.workflow_administration_locators import WorkflowAdministrationLocators

@exception_handler  # Декоратор, обрабатывающий исключения, чтобы тест не прерывался неожиданно
def test_workflow_administration(error_handler, logger, admin_driver):
    """Тест проверяет доступность разедла 'Workflows (адм) - Все задачи (отладка)' и фиксирует ошибки, если они есть."""
    
    logger.info("Начало проверки раздела 'Workflows (адм) - Все задачи (отладка)'")
    # Создаем экземпляр страницы задач с переданным драйвером и логгером
    workflow_administration_page = WorkflowAdministrationPage(admin_driver, logger)

    # Переход в раздел "'Workflows (адм) - Все задачи (отладка)'"
    workflow_administration_page.find_click_header_menu("Workflow (адм)", "Все задачи (отладка)")

    # Проверяем Navigator Listbox со списком задач
    success, details = workflow_administration_page.verify_columns_visibility(WorkflowAdministrationLocators.COLUMN_NAVIGATOR_LISTBOX,WorkflowAdministrationLocators.SCROLLER_NAVIGATION_LISTBOX,
        "check","Задача","isTemplate","isPublished","removed","System","Hidden","isClosed"
    )

    if success:
        logger.info("Проверка видимости колонок прошла успешно.")
    assert success, f"Ошибка проверки видимости колонок: {details}"
