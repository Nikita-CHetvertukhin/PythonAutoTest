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
from selenium.common.exceptions import StaleElementReferenceException

class WorkflowsPage(BasePage):
    """Класс, представляющий страницу "Рабочие процессы" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """
    def create_process(self, name):
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(WorkflowsLocators.WORKFLOWS_CREATE, timeout=5).click()
        self.logger.info("Кнопка 'Создать процесс' нажата")
        textarea = xpath.find_visible(WorkflowsLocators.WORKFLOWS_TEXTAREA, timeout=5)
        self.logger.info("xpath textarea найден")
        textarea.send_keys(name)
        self.logger.info("название процесса введено")
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

    def right_click_and_select_action(self, object_name, action_name, max_retries=5):
        """Находит процесс по имени, кликает ПКМ и выбирает действие из выпадающего списка, 
        обеспечивая устойчивость к изменениям DOM."""
        xpath = XPathFinder(self.driver)
    
        target_xpath = f'{WorkflowsLocators.WORKFLOWS_LIST}/span[@title="{object_name}"]'
        action_xpath = f'{WorkflowsLocators.WORKFLOWS_DROPDOWN}/td[@title="{action_name}"]'

        for attempt in range(max_retries):
            try:
                # Перепроверяем список элементов и ищем процесс
                process_element = xpath.find_located(target_xpath, timeout=10, few=False)

                if process_element:
                    self.logger.info(f"Попытка {attempt + 1}: Процесс '{object_name}' найден.")

                    # Скроллим до элемента
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", process_element)

                    # Ожидание полной загрузки элемента перед взаимодействием
                    WebDriverWait(self.driver, 5).until(EC.visibility_of(process_element))
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(process_element))

                    time.sleep(0.5)  # Небольшая пауза для стабильности

                    # Кликаем ПКМ по элементу
                    actions = ActionChains(self.driver)
                    actions.move_to_element(process_element).perform()
                    actions.context_click(process_element).perform()
                    self.logger.info(f"ПКМ по '{object_name}' выполнен.")

                    # Ожидаем появления контекстного меню
                    action_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, action_xpath))
                    )

                    # Кликаем по нужному пункту меню
                    action_element.click()
                    self.logger.info(f"Действие '{action_name}' выполнено для '{object_name}'.")
                    return True

            except StaleElementReferenceException:
                self.logger.warning(f"Элемент '{object_name}' устарел, пробуем заново...")
                time.sleep(1)  # Ждем, чтобы дать DOM перестроиться

        self.logger.error(f"Не удалось выполнить действие '{action_name}' для '{object_name}' после {max_retries} попыток.")
        return False


