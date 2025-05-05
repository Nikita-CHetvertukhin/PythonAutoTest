from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
#from locators.tasks_tab_locators import TasksTabLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.base_locators import BaseLocators  # Общие локаторы, которые могут использоваться на разных страницах
from utils.exception_handler.decorator_error_handler import exception_handler, MinorIssue

class TasksTabPage(BasePage):

    def checking_succes(self, button_name):
        # Код проверки что текущая нажатая кнопка active (подсвечена розовым)
        # Код проверки что заголовок body соответствует кнопке
        # Код проверки отсутствия всплывающей ошибки
        self.logger.info(f"Кнопка {button_name} обработана успешно")
        return True