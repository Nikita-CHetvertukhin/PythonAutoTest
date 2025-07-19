import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from pages.base_page import BasePage
from locators.my_files_locators import MyFilesLocators
from locators.base_locators import BaseLocators
from utils.element_searching import XPathFinder
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

class MyFilesPage(BasePage):
    
    def upload_file(self, filename):
        xpath = XPathFinder(self.driver)
        wait = WebDriverWait(self.driver, 5)
        UPLOADS_PATH = Path("resources/uploads/workflow")
        file_path = (UPLOADS_PATH / filename).resolve()
        assert file_path.exists(), f"Файл {file_path} не найден."

        create_button = xpath.find_clickable(MyFilesLocators.MY_FILES_CREATE_FILE_BUTTON, timeout=3, few=False)
        create_button.click()
        self.logger.info("Открыта выпадашка 'Создать' в разделе 'Мои файлы'.")

        dropdown_xpath = f'{MyFilesLocators.MY_FILES_CREATE_FILE_DROPDOWN}[contains(@title, "Загрузить файлы")]'
        dropdown_item = xpath.find_clickable(dropdown_xpath, timeout=3, few=False)

        # JS-хук: заранее переопределяем input.click, чтобы подавить системное окно
        self.driver.execute_script("""
            const observer = new MutationObserver(() => {
                const input = document.querySelector('input[type="file"]');
                if (input) {
                    input.click = function() {};  // Отключаем вызов системного окна
                    input.removeAttribute('disabled');
                    input.style.display = 'block';
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
        """)
        self.logger.info("Попытка переопределить input.click до открытия dropdown.")

        dropdown_item.click()
        self.logger.info("Выбрано действие 'Загрузить файлы'.")

        input_field = wait.until(EC.presence_of_element_located((By.XPATH, MyFilesLocators.MY_FILES_UPLOAD_INPUT)))
        self.logger.info(f"Input найден. Сформирован путь: {file_path}")

        # Передаём файл через send_keys
        try:
            input_field.send_keys(str(file_path))
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, input_field)
            self.logger.info(f"Файл {filename} успешно загружен в 'Мои файлы'.")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки файла: {e}")
            raise

    def find_file_by_name(self, name):
        """Ищет процесс по имени и скроллит до него, если он не виден."""
        xpath = XPathFinder(self.driver)

        try:
            # Формируем xpath до интересуещего процесса
            target_xpath = f'{MyFilesLocators.MY_FILES_LIST}/span[@title="{name}"]'

            # Ищем сам элемент внутри списка
            file_element = xpath.find_located(target_xpath, timeout=5, few=False)

            if file_element:
                self.logger.info(f"Файл '{name}' найден в DOM.")

                # Скроллим до элемента
                self.driver.execute_script("arguments[0].scrollIntoView(true);", file_element)

                # Ожидание, чтобы элемент был видимым и доступным для клика
                WebDriverWait(self.driver, 5).until(EC.visibility_of(file_element))
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(file_element))

                self.logger.info(f"Файл '{name}' отображается на экране и доступен")
                return file_element

        except TimeoutException:
            self.logger.warning(f"Файл '{name}' не найден в DOM!")
            return None

    def right_click_and_select_action(self, object_name, action_name, max_retries=5):
        """Находит файл по имени, кликает ПКМ и выбирает действие из выпадающего списка, 
        обеспечивая устойчивость к изменениям DOM."""
        xpath = XPathFinder(self.driver)
    
        target_xpath = f'{MyFilesLocators.MY_FILES_LIST}/span[@title="{object_name}"]'
        action_xpath = f'{MyFilesLocators.MY_FILES_DROPDOWN}/td[@title="{action_name}"]'

        for attempt in range(max_retries):
            try:
                # Перепроверяем список элементов и ищем процесс
                file_element = xpath.find_located(target_xpath, timeout=10, few=False)

                if file_element:
                    self.logger.info(f"Попытка {attempt + 1}: Файл '{object_name}' найден.")

                    # Ожидание полной загрузки элемента перед взаимодействием
                    WebDriverWait(self.driver, 5).until(EC.visibility_of(file_element))
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(file_element))

                    time.sleep(0.5)  # Небольшая пауза для стабильности

                    # Кликаем ПКМ по элементу
                    actions = ActionChains(self.driver)
                    actions.move_to_element(file_element).perform()
                    actions.context_click(file_element).perform()
                    self.logger.info(f"ПКМ по '{object_name}' выполнен.")

                    # Ожидаем появления контекстного меню
                    action_element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, action_xpath))
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

    def create_file(self, file_name, file_type):
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(MyFilesLocators.MY_FILES_CREATE, timeout=5).click()
        self.logger.info("Кнопка 'Создать' нажата")
        xpath.find_clickable(f'{MyFilesLocators.MY_FILES_CREATE_DROPDOWN}[contains(@title, "{file_type}")]',timeout=5).click()
        textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
        self.logger.info("xpath textarea найден")
        textarea.send_keys(file_name)
        self.logger.info("название файла введено")
        textarea.send_keys(Keys.ENTER)
        self.logger.info(f"Имя файла '{file_name}' введено и подтверждено Enter")