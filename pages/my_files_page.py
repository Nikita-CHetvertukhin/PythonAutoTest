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
        """Создает новый файл в разделе 'Мои файлы' с указанным именем и типом.
        Поддерживаемые типы: "Новый документ","Интерактивный шаблон","Новую папку"
        """
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

    def create_folder_in_templates(self, file_name):
        """Создает новую папку в разделе 'Шаблоны' с заданным названием.
        """
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(MyFilesLocators.CREATE_TEMPLATES_FOLDER_BUTTON, timeout=5).click()
        self.logger.info("Кнопка 'Создать' нажата")
        textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
        self.logger.info("xpath textarea найден")
        textarea.send_keys(file_name)
        self.logger.info("название папки введено")
        textarea.send_keys(Keys.ENTER)
        self.logger.info(f"Имя папки '{file_name}' введено и подтверждено Enter")

    def create_docz_from_dotx_section(self, file_name, directory=None, section_name=None):
        '''Метод создаёт анкету из раздела шаблоны и сохраняет её в указанную секцию (опионально) или директорию (опционально), с новым названием (Опционально)
        По умолчанию - Корень Мои файлы, название шаблона'''
        # Ожидаем появления инпута
        input_element = self.xpath.find_clickable(MyFilesLocators.QUESTIONNAIRE_NAME_INPUT, timeout=3, few=False)
        input_element.clear()
        input_element.send_keys(file_name)
        # Кликаем по кнопке "Сохранить здесь"
        self.xpath.find_clickable(MyFilesLocators.QUESTIONNAIRE_CONFIRM_BUTTON, timeout=3, few=False).click()
        self.logger.info(f"Создана анкета с именем '{file_name}'.")

    def create_drive(self, drive_name, side_menu=False):
        """Создает новый общий диск с указанным именем."""
        xpath = XPathFinder(self.driver)
        actions = ActionChains(self.driver)
        if side_menu:
            # Если нужно создать общий диск из бокового меню
            # Наводим крусор на кнопку "Общие диски" в боковом меню
            share_drive_xpath = f'{BaseLocators.SIDE_MENU_BUTTONS}//span[text()="Общие диски"]/ancestor::a'
            share_drive_element = xpath.find_visible(share_drive_xpath, timeout=5)
            actions.move_to_element(share_drive_element).perform()
            self.logger.info("Наведение курсора на кнопку 'Общие диски' в боковом меню выполнено")
            # Создаем общий диск
            xpath.find_clickable(MyFilesLocators.SIDE_MENU_ADD_SHARE_DRIVE, timeout=5).click()
            self.logger.info("Кнопка 'Создать общий диск' нажата")
            textarea = xpath.find_visible(MyFilesLocators.SIDE_MENU_TEXTAREA_SHARE_DRIVE, timeout=5)
            self.logger.info("xpath textarea найден")
            textarea.send_keys(drive_name)
            self.logger.info(f"Имя общего диска '{drive_name}' введено")
            textarea.send_keys(Keys.ENTER)
            self.logger.info(f"Имя общего диска '{drive_name}' подтверждено Enter")
        else:
            xpath.find_clickable(MyFilesLocators.MY_FILES_CREATE, timeout=5).click()
            self.logger.info("Кнопка 'Создать' нажата")
            textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
            self.logger.info("xpath textarea найден")
            textarea.send_keys(drive_name)
            self.logger.info(f"Имя общего диска введено")
            textarea.send_keys(Keys.ENTER)
            self.logger.info(f"Имя общего диска '{drive_name}' подтверждено Enter")