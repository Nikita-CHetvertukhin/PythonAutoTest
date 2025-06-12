from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.my_tasks_locators import MyTasksLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.base_locators import BaseLocators  # Общие локаторы, которые могут использоваться на разных страницах
from utils.element_searching import XPathFinder
from selenium.webdriver.common.keys import Keys

class MyTasksPage(BasePage):
    """Класс, представляющий страницу "Мои задачи" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """

    # Заглушка до появления собственных методов, чтобы не нарушать архитектуру
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        # Инициализация XPathFinder для поиска элементов
        self.xpath = XPathFinder(driver)

    def checking_publish_process(self, process_name):
        """Проверяет публикацию процесса."""
        xpath = XPathFinder(self.driver)

        xpath.find_clickable(MyTasksLocators.MY_TASKS_CREATE_TASK_BUTTON, timeout=5).click()
        self.logger.info("Кнопка 'Создать задачу' нажата")
        input_element = xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_TYPE_INPUT, timeout=5)
        input_element.click()  # Кликаем по полю ввода типа задачи
        input_element.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_element.send_keys(Keys.DELETE)  # Удалить выделенное
        input_element.send_keys(process_name)
        self.logger.info(f"Имя процесса '{process_name}' введено в поле типа задачи")
        if xpath.find_clickable(f'{MyTasksLocators.MY_TASKS_TASK_TYPE_TRS}[contains(@title,"{process_name}")]', timeout=5):
            self.logger.info(f"Процесс '{process_name}' найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return True
        else:
            self.logger.error(f"Процесс '{process_name}' не найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return False