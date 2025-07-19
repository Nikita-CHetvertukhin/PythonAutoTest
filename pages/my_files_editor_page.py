import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from pages.base_page import BasePage
from locators.base_locators import BaseLocators
from locators.my_files_editor_locators import MyFilesEditorLocators
from utils.element_searching import XPathFinder

class MyFilesEditorPage(BasePage):

    # Заглушка до появления собственных методов, чтобы не нарушать архитектуру
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        # Инициализация XPathFinder для поиска элементов
        self.xpath = XPathFinder(driver)

    def find_and_send_variable_in_questionnaire(self, variable_type, variable_name, content):
        '''Метод ищет переменную в анкете по названию и заполняет её textarea'''
        target_box_path = f'{MyFilesEditorLocators.QUESTIONNAIRE_ITEM_NAME}[text()="{variable_name}"]/ancestor::span'
        # Пока просто добавил textarea, но в зависимости от типа переменной может быть input и тд
        textarea_box_path = f'{target_box_path}//textarea'
        if variable_type == "Текст":
            textarea = self.xpath.find_clickable(textarea_box_path, timeout=3)
            textarea.send_keys(content)
