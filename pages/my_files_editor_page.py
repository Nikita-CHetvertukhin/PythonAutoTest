import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
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
        self.actions = ActionChains(driver)

    def waiting_status_after(self, action):
        """
        Метод динамического ожидания готовности документа после открытия или сохранения.
        Проверяет отсутствие ошибки и наличие успешного статуса.

        :param action: str, 'open' или 'save'
        :return: bool, True если статус успешный
        :raises Exception: если обнаружена ошибка или статус не определён
        """
        ok_status_after_open_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Последнее")]'
        save_process_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Сохранение")]'
        ok_status_after_save_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Cохранен")]'
        error_status_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Ошибка")]'

        if action == 'open':
            if self.xpath.find_located(ok_status_after_open_xpath, timeout=5):
                self.logger.info("Документ успешно открыт.")
                return True
            elif self.xpath.find_located(error_status_xpath, timeout=1):
                self.logger.error("Обнаружена ошибка при открытии документа.")
                raise Exception("Обнаружена ошибка при открытии документа")
            else:
                self.logger.error("Таймаут ожидания статуса после открытия.")
                raise Exception("Таймаут ожидания статуса после открытия")

        elif action == 'save':
            if self.xpath.find_located(save_process_xpath, timeout=1):
                if self.xpath.find_located(ok_status_after_save_xpath, timeout=5):
                    self.logger.info("Документ успешно сохранён.")
                    return True
                elif self.xpath.find_located(error_status_xpath, timeout=1):
                    self.logger.error("Обнаружена ошибка при сохранении документа.")
                    raise Exception("Обнаружена ошибка при сохранении документа")
                else:
                    self.logger.error("Таймаут ожидания статуса после сохранения.")
                    raise Exception("Таймаут ожидания статуса после сохранения")
            else:
                self.logger.error(f"Нет актуального статуса сохранения документа: {save_process_xpath}")
                raise Exception(f"Нет актуального статуса сохранения документа {save_process_xpath}")
        else:
            self.logger.error(f"Недопустимое значение параметра action: {action}")
            raise ValueError("Недопустимое значение параметра action: ожидается 'open' или 'save'")

    def click_file_and_click(self, name_action):
        '''Метод кликает по кнопке "Файл" в докмуенте, далее выбирает и кликает указанную кнопку'''
        file_button_xpath = MyFilesEditorLocators.FILE_BUTTON
        target_item_xpath = f'{MyFilesEditorLocators.FILE_BUTTON_TRS}/label[text()="{name_action}"]/ancestor::div[1]'
        
        self.logger.info("Поиск и клик по кнопке Файл")
        self.xpath.find_clickable(file_button_xpath, timeout=3).click()
        self.logger.info(f"Поиск и клик по элементу выпадашки Файла {name_action}")
        self.xpath.find_clickable(target_item_xpath, timeout=3).click()

    def send_text_in_doc(self, text):
        '''Метод отправляет текст в документа в редакторе'''
        input_xpath = MyFilesEditorLocators.DOC_INPUT
        
        input_field = self.xpath.find_located(input_xpath, timeout=3)
        input_field.send_keys(f"{text}")

    def tie_to_schema(self, text, variable_name):
        '''Метод кликает дважды по тексту и привязывает к перемнной'''
        span = self.xpath.find_visible(f"//span[text()='{text}']")
        self.actions.double_click(span).perform()
        self.xpath.find_clickable(MyFilesEditorLocators.EDITOR_TIE).click()
        
        target_variable = f'{MyFilesEditorLocators.SCHEM_VARIABLE_LIST}[contains(@title,"{variable_name}")]/ancestor::tr[1]'
        target = self.xpath.find_visible(target_variable, timeout=3)
        self.actions.double_click(target).perform()
        self.logger.info(f"Выполнена привязка к переменной {variable_name}")

    def open_side_panel_in_doc(self, panel_name):
        '''Открывает боковую панель по названию'''
        target_path = f'{MyFilesEditorLocators.DOC_SIDE_PANEL}[contains(@title,"{panel_name}")]'
        try:
            self.xpath.find_clickable(target_path, timeout=3).click()
            self.logger.info(f"Клик по панели документа {panel_name} выполнен")
            return True
        except Exception:
            self.logger.info(f"Панель документа {panel_name} недоступна")
            return False

    def create_first_variable(self, name):
        '''Кликает создать переменную и присваивает имя'''
        button_xpath = MyFilesEditorLocators.SCHEM_CREATE_FIRST_VARIABLE
        textare_xpath = MyFilesEditorLocators.ACTIVE_TEXTAREA_PANEL

        self.logger.info(f"Попытка создать первую перемнную в схеме с именем {name}")
        self.xpath.find_clickable(button_xpath, timeout=3).click()
        textare_element = self.xpath.find_clickable(textare_xpath, timeout=3)
        textare_element.send_keys(f"{name}")
        self.logger.info(f"Первая переменная с именем {name} добавлена в схему")

    def find_and_send_variable_in_questionnaire(self, variable_type, variable_name, content):
        '''Метод ищет переменную в анкете по названию и заполняет её textarea'''
        target_box_path = f'{MyFilesEditorLocators.QUESTIONNAIRE_ITEM_NAME}[text()="{variable_name}"]/ancestor::span'
        # Пока просто добавил textarea, но в зависимости от типа переменной может быть input и тд
        textarea_box_path = f'{target_box_path}//textarea'
        if variable_type == "Текст":
            textarea = self.xpath.find_clickable(textarea_box_path, timeout=3)
            textarea.send_keys(content)

    def finish_questionnaire(self, action_name):
        '''После заполнения анкеты нажимает "Далее" и выполняет указанное действие'''
        next_button_xpath = MyFilesEditorLocators.QUESTIONNAIRE_FINISH_BUTTON
        target_action_xpath = f'{MyFilesEditorLocators.QUESTIONNAIRE_FINISH_LIST}[text()="{action_name}"]/ancestor::div[contains(@class,"item")]'

        self.logger.info("Клик по кнопке Далее")
        self.xpath.find_clickable(next_button_xpath, timeout=3).click()
        self.logger.info(f"Клик по Действию {action_name}")
        self.xpath.find_clickable(target_action_xpath, timeout=3).click()

    def wf_action_in_file(self, action_name):
        '''Метод октрывает кнопку "Действия" в тулбаре wf документа и кликает по указанному действию'''
        self.xpath.find_clickable(MyFilesEditorLocators.WF_ACTIONS_BUTTON, timeout=3).click()
        action_xpath = f'{MyFilesEditorLocators.WF_ACTIONS_LIST_ITEM}[contains(text(),"{action_name}")]/ancestor::div[1]'
        self.xpath.find_clickable(action_xpath, timeout=3).click()
        self.close_all_windows()
        self.logger.info(f"Выполнено действие WF '{action_name}' в документе.")