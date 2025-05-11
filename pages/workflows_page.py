import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.workflows_locators import WorkflowsLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.base_locators import BaseLocators  # Общие локаторы, которые могут использоваться на разных страницах
from utils.element_searching import XPathFinder

class WorkflowsPage(BasePage):
    """Класс, представляющий страницу "Рабочие процессы" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """
    def create_process(self, name):
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(WorkflowsLocators.WORKFLOWS_CREATE, timeout=3).click()
        self.logger.info("Кнопка 'Создать процесс' нажата")
        textarea = xpath.find_visible(WorkflowsLocators.WORKFLOWS_TEXTAREA, timeout=3)
        textarea.send_keys(name)
        textarea.send_keys(Keys.ENTER)
        self.logger.info(f"Имя процесса '{name}' введено и подтверждено Enter")

    def find_process_by_name(self, name):
        """Ищет процесс по имени и скроллит до него, если он не виден."""
        xpath = XPathFinder(self.driver)

        try:
            # Формируем xpath до интересуещего процесса
            target_xpath = f'{WorkflowsLocators.WORKFLOWS_LIST}/span[@title="{name}"]'

            # Ищем сам элемент внутри списка
            process_element = xpath.find_located(target_xpath, timeout=5, few=False)

            if process_element:
                self.logger.info(f"Процесс '{name}' найден в DOM.")

                # Скроллим до элемента
                self.driver.execute_script("arguments[0].scrollIntoView(true);", process_element)

                # Ожидание, чтобы элемент был видимым и доступным для клика
                WebDriverWait(self.driver, 5).until(EC.visibility_of(process_element))
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(process_element))

                self.logger.info(f"Процесс '{name}' отображается на экране и доступен")
                return process_element

        except TimeoutException:
            self.logger.warning(f"Процесс '{name}' не найден в DOM!")
            return None

    def right_click_and_select_action(self, object_name, action_name):
        """Находит процесс по имени, кликает ПКМ и выбирает действие из выпадающего списка."""
        xpath = XPathFinder(self.driver)

        try:
            # Формируем XPath до интересующего процесса
            target_xpath = f'{WorkflowsLocators.WORKFLOWS_LIST}/span[@title="{object_name}"]'

            # Ищем сам элемент внутри списка
            process_element = xpath.find_located(target_xpath, timeout=10, few=False)

            if process_element:
                self.logger.info(f"Процесс '{object_name}' найден.")

                # Скроллим до элемента
                self.driver.execute_script("arguments[0].scrollIntoView(true);", process_element)

                # Ожидание, чтобы элемент был видимым и доступным для клика
                WebDriverWait(self.driver, 5).until(EC.visibility_of(process_element))
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(process_element))

                time.sleep(0.5)  # Небольшая пауза для стабильности
                # Кликаем ПКМ по элементу
                actions = ActionChains(self.driver)
                actions.move_to_element(process_element).perform()
                actions.context_click(process_element).perform()
                self.logger.info(f"ПКМ по '{object_name}' выполнен.")

                # Ожидание появления выпадающего списка и клика по нужному действию
                action_xpath = f'{WorkflowsLocators.WORKFLOWS_DROPDOWN}/td[@title="{action_name}"]'
                action_element = xpath.find_clickable(action_xpath, timeout=3, few=False)
                action_element.click()
                self.logger.info(f"Действие '{action_name}' выполнено для '{object_name}'.")

                return True

        except TimeoutException:
            self.logger.warning(f"Процесс '{object_name}' или действие '{action_name}' не найдено!")
            return False
