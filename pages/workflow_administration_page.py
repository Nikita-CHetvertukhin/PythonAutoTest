from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.base_locators import BaseLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.workflow_administration_locators import WorkflowAdministrationLocators  # Общие локаторы, которые могут использоваться на разных страницах
from utils.element_searching import XPathFinder

class WorkflowAdministrationPage(BasePage):
    """Класс, представляющий страницу "Мои задачи" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """

    # Заглушка до появления собственных методов, чтобы не нарушать архитектуру
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        # Инициализация XPathFinder для поиска элементов
        self.xpath = XPathFinder(driver)