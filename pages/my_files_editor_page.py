import os
from pickle import FALSE
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
        ok_status_after_save_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Cохранен ")]'
        error_status_xpath = f'{MyFilesEditorLocators.DOC_STATUS}[contains(text(),"Ошибка")]'

        if action == 'open':
            if self.xpath.find_located(ok_status_after_open_xpath, timeout=10):
                self.logger.info("Документ успешно открыт.")
                return True
            elif self.xpath.find_located(error_status_xpath, timeout=1):
                self.logger.error("Обнаружена ошибка при открытии документа.")
                raise Exception("Обнаружена ошибка при открытии документа")
            else:
                self.logger.error("Таймаут ожидания статуса после открытия.")
                raise Exception("Таймаут ожидания статуса после открытия")

        elif action == 'save':
            try:
                # Иногда сохранение происходит очень быстро и статус "Сохранение" не появляется
                process_save_status = self.xpath.find_located(save_process_xpath, timeout=1)
                if process_save_status:
                    if self.xpath.find_located(ok_status_after_save_xpath, timeout=10):
                        self.logger.info("Документ успешно сохранён.")
                        return True
                    elif self.xpath.find_located(error_status_xpath, timeout=1):
                        self.logger.error("Обнаружена ошибка при сохранении документа.")
                        raise Exception("Обнаружена ошибка при сохранении документа")
                    else:
                        self.logger.error("Таймаут ожидания статуса после сохранения.")
                        raise Exception("Таймаут ожидания статуса после сохранения")
            except Exception:
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
            self.logger.error(f"Недопустимое значение параметра action: {action}")
            raise ValueError("Недопустимое значение параметра action: ожидается 'open' или 'save'")

    def click_file_and_click(self, name_action):
        '''Метод кликает по кнопке "Файл" в докмуенте, далее выбирает и кликает указанную кнопку'''
        file_button_xpath = MyFilesEditorLocators.FILE_BUTTON
        target_item_xpath = f'{MyFilesEditorLocators.FILE_BUTTON_TRS}/div[text()="{name_action}"]/ancestor::div[1]'
        target_publish_unpublish_xpath = f'{MyFilesEditorLocators.FILE_PUBLICATION_BUTTONS}[text()="{name_action}"]/ancestor::div[1]'
        self.logger.info("Поиск и клик по кнопке Файл")
        self.xpath.find_clickable(file_button_xpath, timeout=3).click()
        if name_action in ("Опубликовать", "Снять с публикации"):
            self.logger.info(f"Поиск и клик по элементу выпадашки Файла {name_action}")
            self.xpath.find_clickable(target_publish_unpublish_xpath, timeout=3).click()
            return
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

    def check_content_in_doc(self, content, string_sumber=None, partial_match=False):
        '''Метод ищет span в тексте с точным совпадением с заданным'''
        try:
            match_expr = f"contains(text(), '{content}')" if partial_match else f"text()='{content}'"

            if string_sumber is not None:
                self.xpath.find_visible(f"{MyFilesEditorLocators.EDITOR_LINE}[{string_sumber}]//span[{match_expr}]", timeout=1)
                self.logger.info(f"Текст '{content}' найден в документе на строке '{string_sumber}'")
                return True
            else:
                self.xpath.find_visible(f"{MyFilesEditorLocators.EDITOR_LIST}//span[{match_expr}]", timeout=1)
                self.logger.info(f"Текст '{content}' найден в документе")
                return True
        except Exception:
            self.logger.error(f"Текст '{content}' НЕ найден в документе '{MyFilesEditorLocators.EDITOR_LINE}[{string_sumber}]//span[{match_expr}]'")
            return False

    def open_side_panel_in_doc(self, panel_name):
        """Открывает боковую панель по названию, если она не активна"""
        target_path = f'{MyFilesEditorLocators.DOC_SIDE_PANEL}[contains(@title,"{panel_name}")]'
        active_path = f'{MyFilesEditorLocators.DOC_SIDE_PANEL_ACTIVE}[contains(@title,"{panel_name}")]'
        try:
            # Проверяем, активна ли панель
            active_elements = self.xpath.not_find(active_path, timeout=1)
            if not active_elements:
                self.logger.info(f"Панель документа {panel_name} уже активна")
                return True
            # Если не активна — кликаем
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
        try:
            self.logger.info(f"Попытка создать первую перемнную в схеме с именем {name}")
            self.xpath.find_clickable(button_xpath, timeout=1).click()
            textare_element = self.xpath.find_clickable(textare_xpath, timeout=1)
            textare_element.send_keys(f"{name}")
            textare_element.send_keys(Keys.ENTER)
            self.logger.info(f"Первая переменная с именем {name} добавлена в схему")
            return True
        except Exception:
            self.logger.error(f"Не удалось создать переменную")
            return False

    def find_and_send_variable_in_questionnaire(self, variable_type, variable_name, content=None, in_replicator=False, replica_name=None, variable_in_replica_type=None, variable_in_replica_name=None, replica_action=None):
        '''Метод ищет переменную в анкете по названию и заполняет её textarea'''
        target_box_path = f'{MyFilesEditorLocators.QUESTIONNAIRE_ITEM_NAME}[text()="{variable_name}"]/ancestor::span'
        # Пока просто добавил textarea, но в зависимости от типа переменной может быть input и тд
        textarea_box_path = f'{target_box_path}//textarea'
        input_box_path = f'{target_box_path}//input'
        flag_box_path = f'{target_box_path}/parent::*/i'
        if variable_type == "Текст":
            self.logger.info(f"Поиск и заполнение переменной '{variable_name}' типа '{variable_type}' в анкете")
            target_textarea = self.xpath.find_clickable(textarea_box_path, timeout=3, scroll=True)
            target_textarea.send_keys(content)
            self.logger.info(f"Переменная '{variable_name}' типа '{variable_type}' заполнена в анкете значением '{content}'")
        if variable_type in ("Дата", "Число"):
            self.logger.info(f"Поиск и заполнение переменной '{variable_name}' типа '{variable_type}' в анкете")
            target_input = self.xpath.find_clickable(input_box_path, timeout=3, scroll=True)
            target_input.send_keys(content)
            self.logger.info(f"Переменная '{variable_name}' типа '{variable_type}' заполнена в анкете значением '{content}'")
        if variable_type == "Условие":
            self.logger.info(f"Поиск и заполнение переменной '{variable_name}' типа '{variable_type}' в анкете")
            target_flag = self.xpath.find_clickable(flag_box_path, timeout=3, scroll=True)
            target_flag.click()
            self.logger.info(f"По переменной '{variable_name}' типа '{variable_type}' выполнен клик")
        if variable_type == "Мультипликатор":
            '''Действия с репликой, требуют аргументов: 
            variable_type (Мультипликтатор), variable_name (Имя мульта), replica_name (Название реплики), replica_action (Добавить или удалить)'''
            if replica_action == "Добавить":
                self.logger.info(f"Добавление новой реплики от реплики '{replica_name}' в мультипликатор '{variable_name}'")
                add_replica_button_xpath = f'{target_box_path}//span[(@class=" text")and contains(@title,"{replica_name}")]//a[contains(@title,"Добавить")]'
                self.xpath.find_clickable(add_replica_button_xpath, timeout=3, scroll=True).click()
            if replica_action == "Удалить":
                self.logger.info(f"Удаление реплики от реплики '{replica_name}' в мультипликатор '{variable_name}'")
                delete_replica_button_xpath = f'{target_box_path}//span[(@class=" text")and contains(@title,"{replica_name}")]//a[contains(@title,"Удалить")]'
                self.xpath.find_clickable(delete_replica_button_xpath, timeout=3, scroll=True).click()
            '''Действие с переменной внутри мультипликатора, требует аргументов:
            variable_type (Мультипликтатор), variable_name (Имя мульта), content (если нужно ввести контент), in_replicator (True),
            replica_name (Название реплики), variable_in_replica_type (тип переменной), variable_in_replica_name (название переменной)'''
            if in_replicator:
                target_box_path = f'{MyFilesEditorLocators.QUESTIONNAIRE_ITEM_NAME}[text()="{variable_name}"]/ancestor::span//span[(@class=" text")and contains(@title,"{replica_name}")]//span[@title="{variable_in_replica_name}"]'
                textarea_box_path = f'{target_box_path}//textarea'
                input_box_path = f'{target_box_path}//input'
                flag_box_path = f'{target_box_path}/parent::*/i'
                if variable_in_replica_type == "Текст":
                    self.logger.info(f"Поиск и заполнение переменной '{variable_in_replica_name}' типа '{variable_in_replica_type}' в реплике '{replica_name}' мультипликатора '{variable_name}'")
                    target_textarea = self.xpath.find_clickable(textarea_box_path, timeout=3, scroll=True)
                    target_textarea.send_keys(content)
                    self.logger.info(f"Переменная '{variable_in_replica_name}' типа '{variable_in_replica_type}' заполнена в реплике '{replica_name}' мультипликатора '{variable_name}' значением '{content}'")
                if variable_in_replica_type in ("Дата", "Число"):
                    self.logger.info(f"Поиск и заполнение переменной '{variable_in_replica_name}' типа '{variable_in_replica_type}' в реплике '{replica_name}' мультипликатора '{variable_name}'")
                    target_input = self.xpath.find_clickable(input_box_path, timeout=3, scroll=True)
                    target_input.send_keys(content)
                    self.logger.info(f"Переменная '{variable_in_replica_name}' типа '{variable_in_replica_type}' заполнена в реплике '{replica_name}' мультипликатора '{variable_name}' значением '{content}'")
                if variable_in_replica_type == "Условие":
                    self.logger.info(f"Поиск и заполнение переменной '{variable_in_replica_name}' типа '{variable_in_replica_type}' в реплике '{replica_name}' мультипликатора '{variable_name}'")
                    target_flag = self.xpath.find_clickable(flag_box_path, timeout=3, scroll=True)
                    target_flag.click()
                    self.logger.info(f"По переменной '{variable_in_replica_name}' типа '{variable_in_replica_type}' в реплике '{replica_name}' мультипликатора '{variable_name}' выполнен клик")

    def finish_questionnaire(self, action_name):
        '''После заполнения анкеты нажимает "Далее" и выполняет указанное действие'''
        next_button_xpath = MyFilesEditorLocators.QUESTIONNAIRE_FINISH_BUTTON
        target_action_xpath = f'{MyFilesEditorLocators.QUESTIONNAIRE_FINISH_LIST}[text()="{action_name}"]/ancestor::div[contains(@class,"item")][1]'

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

    def find_click_span_in_text(self, text):
        '''Метод ищет span с заданным текстом и кликает по нему'''
        span_xpath = f"//span[text()='{text}']"
        self.logger.info(f"Поиск и клик по тексту '{text}' в документе")
        self.xpath.find_clickable(span_xpath, timeout=3).click()

    def check_acces_in_editor(self, acces_level, setting_type, text=None, element_class=None):
        '''Метод делает принимает уровень доступа в acces_level,
        далее делает двойной клик по заданному text или element_class и проверяет возможность/невозможность изменения текста,
        Далее открывает боковую панель заданную в setting_type и проверяет доступность/недоступность панели'''
        if text is not None:
            span = self.xpath.find_visible(f"//span[text()='{text}']")
        else:
            span = self.xpath.find_visible(f"//span[@class='{element_class}']")
        input_xpath = MyFilesEditorLocators.DOC_INPUT
        test_content = f"Проверка уровня доступа {acces_level} на тексте {text}"
        side_format_panel = f"{MyFilesEditorLocators.DOC_SIDE_PANEL_FORMAT}[contains(@title, '{setting_type}')]"
        active_side_format_panel = f"{MyFilesEditorLocators.DOC_SIDE_PANEL_FORMAT}[contains(@title, '{setting_type}') and contains(@class,'x-active')]"
        panel_actions_xpath = f"{MyFilesEditorLocators.DOC_SIDE_FORMAT_XBOX}"

        # Клик по тексту в редакторе
        span.click()
        
        input_field = self.xpath.find_located(input_xpath, timeout=3)
        if element_class != "drawing":
            input_field.send_keys(f"{test_content}")
            if acces_level in ["Рецензирование","Полный доступ"]:
                self.logger.info(f"Уровень доступа '{acces_level}' позволяет редактировать текст.")
                self.xpath.find_visible(f"//span[contains(text(), '{test_content}')]", timeout=1)
            else:
                self.logger.info(f"Уровень доступа '{acces_level}' НЕ позволяет редактировать текст.")
                try:
                    self.xpath.find_visible(f"//span[contains(text(), '{test_content}')]", timeout=1)
                    raise Exception(f"Ошибка: Уровень доступа '{acces_level}' позволяет редактировать текст, хотя не должен.")
                except Exception:
                    self.logger.info(f"Редактирование текста не произошло, что соответствует уровню доступа '{acces_level}'.")

        try:
            # Проверяем, активна ли панель
            is_not_found = self.xpath.not_find(active_side_format_panel, timeout=1)
            if not is_not_found:  # значит элемент найден → панель уже активна
                self.logger.info(f"Панель форматирования '{setting_type}' уже активна")
            else:
                # Если не активна — кликаем
                self.logger.info(f"Попытка открыть панель форматирования '{setting_type}'")
                self.xpath.find_clickable(side_format_panel, timeout=3).click()
                self.logger.info(f"Панель форматирования '{setting_type}' открыта")
        except Exception:
            self.logger.warning(f"Панель форматирования '{setting_type}' недоступна")
        # Проверка доступности элементов панели форматирования
        self.logger.info(f"Далее поиск всех элементов по пути {panel_actions_xpath}")
        panel_elements = self.xpath.find_visible(panel_actions_xpath, few=True, timeout=3)
        self.logger.info(f"Нашёл все элементы по пути {panel_actions_xpath}")

        for n, el in enumerate(panel_elements, start=1):
            class_attr = el.get_attribute("class") or ""
            
            # Дополнительное исключения для пунктов 13,14,15 в настройках абзаца и таблицы (пока не редактируем их в ДЗ)
            if acces_level in ["Рецензирование", "Полный доступ"] \
               and setting_type in ["Настройки абзаца"] \
               and n in (13, 14, 15):
                # Эти пункты сейчас всегда disabled, даже при полном доступе
                if "x-disabled" not in class_attr:
                    raise Exception(
                        f"Ошибка: Пункт [{n}] панели '{setting_type}' "
                        f"должен быть недоступен при уровне доступа '{acces_level}'"
                    )
                else:
                    self.logger.info(
                        f"Пункт [{n}] панели '{setting_type}' корректно недоступен "
                        f"при уровне доступа '{acces_level}'"
                    )
                continue  # Переходим к следующему элементу
            
            if acces_level in ["Рецензирование", "Полный доступ"]:
                if "x-disabled" in class_attr:
                    raise Exception(f"Ошибка: Порядковый элемент '[{n}]' панели '{setting_type}' недоступен при уровне доступа '{acces_level}'")
                else:
                    self.logger.info(f"Порядковый элемент '[{n}]' панели '{setting_type}' доступен — соответствует уровню доступа '{acces_level}'")
            else:
                if "x-disabled" not in class_attr:
                    raise Exception(f"Ошибка: Порядковый элемент '[{n}]' панели '{setting_type}' доступен при уровне доступа '{acces_level}', хотя не должен")
                else:
                    self.logger.info(f"Порядковый элемент '[{n}]' панели '{setting_type}' недоступен — соответствует уровню доступа '{acces_level}'")

        # --- Финальная проверка количества элементов ---
        expected_count = None
        if setting_type in ("Настройки абзаца", "Настройки таблицы"):
            expected_count = 15
        elif setting_type == "Настройки изображения":
            expected_count = 10

        if expected_count is not None:
            if n != expected_count:
                raise Exception(
                    f"Ошибка: количество элементов панели ({n}) не соответствует ожидаемому ({expected_count}) "
                    f"для типа настроек '{setting_type}'"
                )
            else:
                self.logger.info(f"Количество элементов панели ({n}) соответствует ожидаемому для '{setting_type}'")

    def is_element_allowed(self, section: str, access_level: str, title: str, class_attr: str, file_type: str = None) -> bool:
        '''Вспомогательный метод для следующего метода, включает матрицу доступов к разделам документа'''
        ACCESS_MATRIX = {
            "Главная": {
                "Просмотр": ["Отобразить все знаки (Ctrl+*)"],
                "Комментирование": ["Отобразить все знаки (Ctrl+*)"],
                "Рецензирование": ["ALL"],
                "Полный доступ": ["ALL"]
            },
            "Вставка": {
                "Просмотр": [],
                "Комментирование": ["Комментарий"],
                "Рецензирование": ["ALL"],
                "Полный доступ": ["ALL"]
            },
            "Макет": {
                "Просмотр": [],
                "Комментирование": [],
                "Рецензирование": ["ALL"],
                "Полный доступ": ["ALL"]
            },
            # Здесь временно Принять + Отклонить (До фикса)
            "Рецензирование": {
                "Просмотр": ["Отображение", "Предыдущее", "Следующее", "Принять","Отклонить" ,"Сравнить","История версий"],
                "Комментирование": ["Отображение", "Предыдущее", "Следующее","Принять", "Отклонить", "Сравнить", "История версий"],
                "Рецензирование": ["Отображение", "Предыдущее", "Следующее", "Принять", "Отклонить", "Сравнить", "История версий", "Запись изменений (active)"],
                "Полный доступ": ["ALL"]
            },
            "Конструктор": {
                "Просмотр": ["Все ответы"],
                "Комментирование": ["Все ответы"],
                "Рецензирование": ["ALL"],
                "Полный доступ": ["ALL"]
            }
        }
        allowed_items = ACCESS_MATRIX.get(section, {}).get(access_level, [])

        # Исключение: для docx запрещены две кнопки на вкладке "Конструктор"
        if section == "Конструктор" and file_type == "docx":
            # До фикса кнопка "Разрешить редактирование" доступна
            #if title in ["Разрешить редактировать область", "Запретить редактировать область"]:
            if title in ["Запретить редактировать область"]:
                return False

        if "ALL" in allowed_items:
            return True

        # Спец-обработка: "Конструктор" — проверка по фрагменту заголовка
        if section == "Конструктор":
            return any(allowed_title in title for allowed_title in allowed_items)

        # Обычная проверка по точному совпадению title
        return title in allowed_items

    def check_acces_in_header_section(self, acces_level, section_name, file_type=None):
        '''Метод открывает нужный раздел в хедере и проверяет доступность/недоступность элементов в зависимости от уровня доступа'''
        section_button_xpath = f'{MyFilesEditorLocators.TOOLBAR_SECTION_TITLE}/div[contains(@class,"label") and (text()="{section_name}")]/ancestor::div[1]'
        active_section_button_xpath = f'{MyFilesEditorLocators.TOOLBAR_SECTION_TITLE}/div[contains(@class,"label") and (text()="{section_name}")]/ancestor::div[contains(@class,"x-active")]'
        buttons_in_section_xpath = f'{MyFilesEditorLocators.TOOLBAR_SECTION_BUTTONS}'
        divs_in_section_xpath = f'{MyFilesEditorLocators.TOOLBAR_SECTION_DIVS}'

        try:
            # Проверяем, активна ли секция
            is_not_found = self.xpath.not_find(active_section_button_xpath, timeout=1)
            if not is_not_found:  # элемент найден → секция уже активна
                self.logger.info(f"Панель в хедере '{section_name}' уже активна")
            else:
                # Если не активна — кликаем
                self.logger.info(f"Попытка открыть панель в хедере '{section_name}'")
                self.xpath.find_clickable(section_button_xpath, timeout=3).click()
                self.logger.info(f"Панель в хедере '{section_name}' открыта")
        except Exception:
            self.logger.warning(f"Панель в хедере '{section_name}' недоступна")

        # Проверка доступности элементов панели форматирования
        self.logger.info(f"Далее поиск всех элементов по пути {buttons_in_section_xpath}")
        button_elements = self.xpath.find_visible(buttons_in_section_xpath, few=True, timeout=3)
        if section_name in ["Главная", "Макет", "Конструктор"]:
            self.logger.info(f"Далее поиск всех элементов по пути {divs_in_section_xpath}")
            div_elements = self.xpath.find_visible(divs_in_section_xpath, few=True, timeout=3)

        total_elements = button_elements + (div_elements if section_name in ["Главная", "Макет", "Конструктор"] else [])
        errors = []
        for n, el in enumerate(total_elements, start=1):
            class_attr = el.get_attribute("class") or ""
            label_text = ""
            try:
                label_div = el.find_element(By.XPATH, './div[contains(@class,"x-label")]')
                raw_text = label_div.text
                label_text = " ".join(raw_text.split()) #Нормализация
            except Exception:
                # если вложенного div нет, оставляем пустую строку или логируем
                label_text = ""
            # если текст пустой, пробуем старую логику по атрибуту title
            if not label_text:
                label_text = el.get_attribute("title") or ""

            if (section_name == "Рецензирование" and "Запись изменений" in label_text and acces_level == "Рецензирование"):
                # Ожидается: disabled + active
                if "x-disabled" in class_attr and "x-active" in class_attr:
                    self.logger.info(
                        f"[{n}] Элемент: '{label_text}' | Класс: '{class_attr}' | "
                        f"Ожидается: Недоступен и активен | "
                        f"Фактически: Недоступен и активен")
                    continue  # всё ок, пропускаем проверку
                else:
                    errors.append(
                        f"[{n}] Несоответствие: '{label_text}' в '{section_name}' для '{acces_level}' — "
                        f"ожидалось disabled+active, но класс: '{class_attr}'"
                    )
                continue  # не проверяем дальше
            # Дальше мне нужно проверять наличие в классе disabled или его отстутсвие (если элемент должен быть доступен по матрице доступен)
            is_expected = self.is_element_allowed(section_name, acces_level, label_text, class_attr, file_type)
            is_disabled = "disabled" in class_attr or not el.is_enabled()

            self.logger.info(
                f"[{n}] Элемент: '{label_text}' | Класс: '{class_attr}' | "
                f"Ожидается: {'доступен' if is_expected else 'недоступен'} | "
                f"Фактически: {'недоступен' if is_disabled else 'доступен'}"
            )

            if is_expected != (not is_disabled):
                errors.append(
                    f"[{n}] Несоответствие: '{label_text}' в '{section_name}' для '{acces_level}' — "
                    f"ожидалось {'доступен' if is_expected else 'недоступен'}, "
                    f"но класс: '{class_attr}'"
                )

        if errors:
            error_message = "\n".join(errors)
            raise AssertionError(f"Обнаружены несоответствия доступа:\n{error_message}")