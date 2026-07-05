import os
import time
import allure
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from pages.base_page import BasePage
from locators.my_files_locators import MyFilesLocators
from locators.base_locators import BaseLocators
from utils.element_searching import XPathFinder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

class MyFilesPage(BasePage):

    @allure.step("ПКМ по {object_name} и выбор действия {action_name}")
    def right_click_and_select_action(self, object_name, action_name, max_retries=5):
        """Находит файл по имени, кликает ПКМ и выбирает действие из выпадающего списка, 
        обеспечивая устойчивость к изменениям DOM."""
        xpath = XPathFinder(self.driver)
    
        target_xpath = f'{MyFilesLocators.MY_FILES_LIST}/span[text()="{object_name}"]'
        action_xpath = f'{MyFilesLocators.MY_FILES_DROPDOWN}/td[@title="{action_name}"]'

        for attempt in range(max_retries):
            try:
                # Перепроверяем список элементов и ищем процесс
                file_element = xpath.find_located(target_xpath, timeout=10, few=False)

                if file_element:
                    self.logger.debug(f"Попытка {attempt + 1}: Файл '{object_name}' найден.")

                    # Ожидание полной загрузки элемента перед взаимодействием
                    xpath.wait_visible(file_element, timeout=5)
                    xpath.wait_clickable(file_element, timeout=5)

                    time.sleep(0.5)  # Небольшая пауза для стабильности

                    # Кликаем ПКМ по элементу
                    actions = ActionChains(self.driver)
                    actions.move_to_element(file_element).perform()
                    actions.context_click(file_element).perform()
                    self.logger.debug(f"ПКМ по '{object_name}' выполнен.")

                    # Ожидаем появления контекстного меню
                    action_element = xpath.find_clickable(action_xpath, timeout=5)

                    # Кликаем по нужному пункту меню
                    action_element.click()
                    self.logger.debug(f"Действие '{action_name}' выполнено для '{object_name}'.")
                    return True

            except StaleElementReferenceException:
                self.logger.warning(f"Элемент '{object_name}' устарел, пробуем заново...")
                time.sleep(1)  # Ждем, чтобы дать DOM перестроиться

        self.logger.error(f"Не удалось выполнить действие '{action_name}' для '{object_name}' после {max_retries} попыток.")
        return False

    def get_action_availability(self, file_type, access_level, collaboration_enabled=True):
        '''Метод формирует доступные и недоступные действия по ПКМ в зависимости от типа файла, уровня доступа и лицензии'''

        is_editor = access_level == "Полный доступ"
        is_docx_or_dotx = file_type in ["docx", "dotx"]
        is_docz = file_type == "docz"
        is_folder = file_type == "folder"

        # Допустимые действия по типу файла
        allowed_actions_by_type = {
            "docx": [
                "Открыть", "Открыть в новой вкладке", "Настроить доступ", "Копировать ссылку", "Скачать",
                "Скачать PDF", "Скачать PDF/A", "Загрузить версию", "Сравнить",
                "Копировать", "Переименовать", "Удалить"
            ],
            "dotx": [
                "Открыть", "Открыть в новой вкладке", "Настроить доступ", "Скопировать ссылку", "Скачать",
                "Скачать PDF", "Скачать PDF/A", "Загрузить версию", "Сравнить",
                "Копировать", "Переименовать", "Удалить"
            ],
            "docz": [
                "Открыть", "Открыть в новой вкладке", "Настроить доступ", "Скопировать ссылку", "Скачать",
                "Скачать PDF", "Скачать PDF/A", "Сравнить",
                "Копировать", "Переименовать", "Удалить"
            ],
            "folder": [
                "Открыть", "Открыть в новой вкладке", "Настроить доступ", "Скопировать ссылку",
                "Копировать", "Переименовать", "Удалить"
            ]
        }

        # Получаем допустимые действия
        allowed_actions = allowed_actions_by_type.get(file_type, [])

        availability = {}

        for action in allowed_actions:
            if action == "Открыть":
                availability[action] = True
            elif action == "Открыть в новой вкладке":
                availability[action] = True
            elif action == "Настроить доступ":
                availability[action] = True
            elif action == "Скопировать ссылку":
                availability[action] = True
            elif action == "Скачать":
                availability[action] = True
            elif action in ["Скачать PDF", "Скачать PDF/A"]:
                availability[action] = True
            elif action == "Загрузить версию":
                availability[action] = is_editor and is_docx_or_dotx
            elif action == "Сравнить":
                availability[action] = True
            elif action == "Копировать":
                availability[action] = not is_folder
            elif action == "Переименовать":
                availability[action] = is_editor
            elif action == "Удалить":
                availability[action] = True

        self.logger.info(
            f"Доступные действия для файла типа '{file_type}' с уровнем доступа '{access_level}' (лицензия COLLABORATION {'включена' if collaboration_enabled else 'выключена'}): {availability}")
        return availability
    
    @allure.step("ПКМ по {file_name} и проверка доступности действий")
    def right_click_and_check_acces(self, file_name, result):
        '''Метод ищет файл по имени в текущем разделе, кликает ПКМ и проверяет доступность действий в соответсвии с уровнем доступа'''
        xpath = XPathFinder(self.driver)

        # xpath до самого файла, по которому будем кликать ПКМ
        target_xpath = f'{MyFilesLocators.MY_FILES_LIST}/span[text()="{file_name}"]'

        try:
            # Перепроверяем список элементов и ищем процесс
            file_element = xpath.find_located(target_xpath, timeout=10, few=False)
            # Путь до действия по завершению проверки
            in_end = "Открыть"
            end_action_xpath = f'{MyFilesLocators.MY_FILES_DROPDOWN}/td[@title="{in_end}"]'

            if file_element:
                self.logger.debug(f"Файл '{file_name}' найден.")

                # Ожидание полной загрузки элемента перед взаимодействием
                xpath.wait_visible(file_element, timeout=5)
                xpath.wait_clickable(file_element, timeout=5)

                time.sleep(0.5)  # Небольшая пауза для стабильности

                # Кликаем ПКМ по элементу
                actions = ActionChains(self.driver)
                actions.move_to_element(file_element).perform()
                actions.context_click(file_element).perform()
                self.logger.debug(f"ПКМ по '{file_name}' выполнен.")

                # Проверка доступности действий
                errors = []

                for action_name, expected_status in result.items():
                    action_xpath = f'{MyFilesLocators.MY_FILES_DROPDOWN}/td[@title="{action_name}"]/ancestor::tr'

                    try:
                        action_element = self.xpath.find_located(action_xpath, timeout=3, few=False)
                        if not action_element:
                            errors.append(f"'{action_name}' не найден.")
                            continue

                        class_attr = action_element.get_attribute("class")
                        has_disabled = "disabled" in class_attr.split()

                        if expected_status:
                            if has_disabled:
                                errors.append(f"'{action_name}' должно быть доступно, но содержит класс 'disabled'.")
                            else:
                                self.logger.debug(f"'{action_name}' доступно и кликабельно, класс 'disabled' отсутствует.")
                        else:
                            if has_disabled:
                                self.logger.debug(f"'{action_name}' содержит класс 'disabled'.")
                            else:
                                errors.append(f"'{action_name}' должно быть недоступно, но класс 'disabled' отсутствует.")
                    except Exception as e:
                        errors.append(f"Ошибка при проверке '{action_name}': {str(e)}")

                # После цикла — выбрасываем все ошибки
                if errors:
                    for err in errors:
                        self.logger.error(err)
                    raise AssertionError("Обнаружены ошибки в доступности действий:\n" + "\n".join(errors))
                else:
                    self.logger.debug(f"Все действия для '{file_name}' соответствуют ожиданиям.")
                    # Ожидаем появления контекстного меню
                    action_element = xpath.find_clickable(end_action_xpath, timeout=5)
                    # Кликаем по нужному пункту меню
                    action_element.click()
                    self.logger.debug(f"Действие '{in_end}' выполнено для '{file_name}'.")
                    return True

        except Exception:
            self.logger.error(f"Не удалось кликнуть ПКМ для '{file_name}'.")
            raise

    @allure.step("Создание файла {file_name} типа {file_type}")
    def create_file(self, file_name, file_type):
        """Создает новый файл в разделе 'Мои файлы' с указанным именем и типом.
        Поддерживаемые типы: "Новый документ","Интерактивный шаблон","Новую папку"
        """
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(MyFilesLocators.MY_FILES_CREATE, timeout=5).click()
        self.logger.debug("Кнопка 'Создать' нажата")
        xpath.find_clickable(f'{MyFilesLocators.MY_FILES_CREATE_DROPDOWN}[contains(@title, "{file_type}")]',timeout=5).click()
        textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
        self.logger.debug("xpath textarea найден")
        textarea.send_keys(file_name)
        self.logger.debug("название файла введено")
        textarea.send_keys(Keys.ENTER)
        self.logger.debug(f"Имя файла '{file_name}' введено и подтверждено Enter")

    @allure.step("Создание папки {file_name} в разделе Шаблоны")
    def create_folder_in_templates(self, file_name):
        """Создает новую папку в разделе 'Шаблоны' с заданным названием.
        """
        xpath = XPathFinder(self.driver)
        xpath.find_clickable(MyFilesLocators.CREATE_TEMPLATES_FOLDER_BUTTON, timeout=5).click()
        self.logger.debug("Кнопка 'Создать' нажата")
        textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
        self.logger.debug("xpath textarea найден")
        textarea.send_keys(file_name)
        self.logger.debug("название папки введено")
        textarea.send_keys(Keys.ENTER)
        self.logger.debug(f"Имя папки '{file_name}' введено и подтверждено Enter")

    @allure.step("Создание анкеты {file_name} из шаблона")
    def create_docz_from_dotx_section(self, file_name, directory=None, section_name=None):
        '''Метод создаёт анкету из раздела шаблоны и сохраняет её в указанную секцию (опионально) или директорию (опционально), с новым названием (Опционально)
        По умолчанию - Корень Мои файлы, название шаблона'''
        # Ожидаем появления инпута
        input_element = self.xpath.find_clickable(MyFilesLocators.QUESTIONNAIRE_NAME_INPUT, timeout=3, few=False)
        input_element.clear()
        input_element.send_keys(file_name)
        # Кликаем по кнопке "Сохранить здесь"
        self.xpath.find_clickable(MyFilesLocators.QUESTIONNAIRE_CONFIRM_BUTTON, timeout=3, few=False).click()
        self.logger.debug(f"Создана анкета с именем '{file_name}'.")

    @allure.step("Создание общего диска {drive_name}")
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
            self.logger.debug("Наведение курсора на кнопку 'Общие диски' в боковом меню выполнено")
            # Создаем общий диск
            xpath.find_clickable(MyFilesLocators.SIDE_MENU_ADD_SHARE_DRIVE, timeout=5).click()
            self.logger.debug("Кнопка 'Создать общий диск' нажата")
            textarea = xpath.find_visible(MyFilesLocators.SIDE_MENU_TEXTAREA_SHARE_DRIVE, timeout=5)
            self.logger.debug("xpath textarea найден")
            textarea.send_keys(drive_name)
            self.logger.debug(f"Имя общего диска '{drive_name}' введено")
            textarea.send_keys(Keys.ENTER)
            self.logger.debug(f"Имя общего диска '{drive_name}' подтверждено Enter")
        else:
            xpath.find_clickable(MyFilesLocators.MY_FILES_CREATE, timeout=5).click()
            self.logger.debug("Кнопка 'Создать' нажата")
            textarea = xpath.find_visible(MyFilesLocators.MY_FILES_TEXTAREA, timeout=5)
            self.logger.debug("xpath textarea найден")
            textarea.send_keys(drive_name)
            self.logger.debug(f"Имя общего диска введено")
            textarea.send_keys(Keys.ENTER)
            self.logger.debug(f"Имя общего диска '{drive_name}' подтверждено Enter")