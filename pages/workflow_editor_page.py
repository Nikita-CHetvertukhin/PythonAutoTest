from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.workflow_editor_locators import WorkflowEditorLocators
from utils.element_searching import XPathFinder
from selenium.webdriver.common.action_chains import ActionChains
from settings.variables import USER1_LOGIN

class WorkflowEditorPage(BasePage):
    """Класс, представляющий страницу "Редактор рабочего процесса" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """

    def verify_process_name(self, name):
        """Проверяет, что атрибут title у элемента соответствует ожидаемому name."""
        xpath = XPathFinder(self.driver)
        try:
            self.logger.info(f'Начало поиска элемента по xpath {WorkflowEditorLocators.WFEDITOR_PROPERTIES_NAME}[contains(@title,"{name}")]')
            label_element = xpath.find_located(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_NAME}[contains(@title,"{name}")]', timeout=3)
            self.logger.info(f"Элемент с названием процесса {name} найен")
            
            label_title = label_element.get_attribute("title").strip()
            if label_title == name:
                self.logger.info(f"Название процесса в title совпадает: '{label_title}' == '{name}'")
                return True
            else:
                self.logger.warning(f"Несовпадение title у процесса: '{label_title}' != '{name}'")
                return False

        except Exception as e:
            self.logger.error(f"Ошибка при проверке title у процесса: {e}")
            return False

    def action_from_document(self, action_name):
        """Нажимает 'Файл', внутри документа и кликает по элементу action_name"""
        xpath = XPathFinder(self.driver)
        
        self.logger.info("Клик по кнопке 'Файл'")
        action_button = xpath.find_visible(WorkflowEditorLocators.WFEDITOR_FILE_BUTTON, timeout=1)
        action_button.click()

        self.logger.info(f"Клик по кнопке {action_name}")
        action_xpath = xpath.find_located(f'{WorkflowEditorLocators.WFEDITOR_FILE_DROPDOWN}/div/label[text()="{action_name}"]/parent::div', timeout=3, few=False)
        action_xpath.click()
        if action_name in {"Опубликовать", "Снять с публикации"}:
            self.close_all_windows()

    def add_shape(self, shape_name):
        """Добавляет фигуру в редактор рабочего процесса, проверяет её наличие и возвращает уникальный model_id."""
        xpath = XPathFinder(self.driver)
        shape_mapping = {
            "Вход": "entry",
            "Выход": "exit",
            "Задача": "task",
            "Условие": "decision",
            "Разветвление": "brancher",
            "Слияние": "merger"
        }
        model_class = shape_mapping.get(shape_name, "")

        if not model_class:
            self.logger.warning(f"Неизвестная фигура '{shape_name}', model_class не установлен")
            return None

        g_element_xpath = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@class, "{model_class}")]'

        try:
            # Поиск всех g-элементов данного класса до клика
            existing_elements = self.driver.find_elements(By.XPATH, g_element_xpath)  
            existing_model_ids = [el.get_attribute("model-id") for el in existing_elements] if existing_elements else []

            self.logger.info(f"Клик по кнопке добавления фигуры '{shape_name}' ({model_class})")
            shape_button = xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_SHAPE_BUTTONS}/a[@title="{shape_name}"]', timeout=5)
            shape_button.click()
            self.logger.info(f"Фигура '{shape_name}' ({model_class}) добавлена в редактор рабочего процесса")

            # Ожидание появления нового элемента
            WebDriverWait(self.driver, 5).until(
                lambda driver: len(self.driver.find_elements(By.XPATH, g_element_xpath)) > len(existing_model_ids)
            )

            # Получаем обновленный список всех g-элементов
            updated_elements = self.driver.find_elements(By.XPATH, g_element_xpath)

            # Вычисляем разницу по model-id, чтобы найти новый элемент
            new_model_id = None
            for el in updated_elements:
                model_id = el.get_attribute("model-id")
                if model_id and model_id not in existing_model_ids:
                    new_model_id = model_id
                    break

            if new_model_id:
                self.logger.info(f"Извлечен УНИКАЛЬНЫЙ model_id: {new_model_id} для фигуры {model_class}")
                return new_model_id
            else:
                self.logger.warning(f"Не удалось найти новый g-элемент с классом '{model_class}'")
                return None

        except Exception as e:
            self.logger.error(f"Ошибка при добавлении фигуры '{shape_name}': {e}")
            return None

    def drag_element_right(self, model_id, offset=150):
        xpath = XPathFinder(self.driver)
        action = ActionChains(self.driver)
        shape_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{model_id}")]'
        element = xpath.find_clickable(shape_path)

        # Инициализация ActionChains для выполнения drag-and-drop
        action.click_and_hold(element).move_by_offset(offset, 0).release().perform()
        self.logger.info(f'Элемент {model_id} сдвинут вправо на {offset}')

    def hover_shape(self, model_id):
        xpath = XPathFinder(self.driver)
        action = ActionChains(self.driver)
        shape_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{model_id}")]'
    
        # Ожидание, пока элемент станет доступным
        element = xpath.find_visible(shape_path, timeout=3)

        # Выполнение наведения курсора
        action.move_to_element(element).perform()
        self.logger.info(f'Наведен курсор на {model_id}')

    def click_shape(self, model_id):
        xpath = XPathFinder(self.driver)
        shape_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{model_id}")]'

        # Ожидание, пока элемент станет доступным
        element = xpath.find_visible(shape_path, timeout=3)

        # Выполнение клика напрямую
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.logger.info(f'Клик по {model_id}')

    def click_shape_by_text(self, text):
        """Метод кликаем по фигуре на основани и текста (подходит не для всех фигур, толкьо с аргументом text)"""
        xpath = XPathFinder(self.driver)
        shape_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"]/*[name()="text"][contains(@text,"{text}")]/ancestor::*[name()="g"][1]'
        # Ожидание, пока элемент станет доступным
        element = xpath.find_visible(shape_path, timeout=3)
        # Выполнение клика напрямую
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.logger.info(f'Клик по фигуре с текстом {text}')

    def change_catalog_in_auto(self, type_auto, type_section, name_catalog=None):
        """Метод устанавливает каталог в автоматизациях при старте/завершении, поддерживает аргументы:
        type_auto: "start", "finish" - тип автоматизации (при старте или при завершении)
        type_section: "Мои файлы", "Доступные мне", "Общие диски" - тип секции
        name_catalog: "имя каталога", если нужно выбрать конкретный каталог
        """
        VALID_AUTOS = {"start", "finish"}
        VALID_SECTIONS = {"Мои файлы", "Доступные мне", "Общие диски"}

        if type_auto not in VALID_AUTOS:
            raise ValueError(f"Недопустимое значение type_auto: '{type_auto}'. Допустимые: {VALID_AUTOS}")
        if type_section not in VALID_SECTIONS:
            raise ValueError(f"Недопустимое значение type_section: '{type_section}'. Допустимые: {VALID_SECTIONS}")

        xpath = XPathFinder(self.driver)
        action = ActionChains(self.driver)
        
        # Клик по иконке каталога в зависимости от типа автоматизации
        if type_auto == "start":
            icon = xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_START_AUTO_FOLDER_ICON, timeout=3).click()
        if type_auto == "finish":
            icon = xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_FINISH_AUTO_FOLDER_ICON, timeout=3).click()
        self.logger.info(f'Клик по иконке каталога в автоматизации {type_auto}')
        
        # Выбор секции каталога
        target_section = xpath.find_clickable(
            f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_CATALOG_SECTIONS}[contains(text(), "{type_section}")]/ancestor::a', timeout=3)
        target_section.click()
        self.logger.info(f'Клик по секции {type_section}')
        time.sleep(1)  # Пауза для стабильности
        
        # Если указан каталог, ищем его в списке и делаем двойной клик
        if name_catalog:
            xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_CATALOG_ITEMS}[contains(@title,"{name_catalog}")]/ancestor::tr', timeout=3).click()
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)  # Пауза для стабильности
            self.logger.info(f'Двойной клик по каталогу {name_catalog}')
        
        # Подтверждаем выбор
        xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_CATALOG_SELECT, timeout=3).click()
        time.sleep(0.5)  # Пауза для стабильности
        self.logger.info('Клик по кнопке "Выбрать" в каталоге')

    def connect_shapes(self, first_model_id, second_model_id):
        xpath = XPathFinder(self.driver)
        action = ActionChains(self.driver)

        # Наведение курсора на первую фигуру
        self.hover_shape(first_model_id)
    
        # Поиск исходного элемента
        source_element = xpath.find_visible(
            f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{first_model_id}")]/*[name()="g"]',
            timeout=3
        )
        self.logger.info(f'Исходный элемент {first_model_id} найден')

        # Начинаем drag-and-drop
        action.click_and_hold(source_element).perform()

        # Динамический поиск элемента в процессе drag
        dynamic_element = xpath.find_visible(
            f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@style, "events")]',
            timeout=3
        )

        # Получаем model-id найденного элемента
        dynamic_model_id = dynamic_element.get_attribute("model-id")
        self.logger.info(f'Идентификатор элемента связи установлен {dynamic_model_id}')

        # Завершаем перемещение к целевой фигуре
        target_element = xpath.find_visible(
            f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{second_model_id}")]',
            timeout=3
        )
        action.move_to_element(target_element).release().perform()
        self.logger.info(f'Связь с элементом {second_model_id} установлена')

       # Выполнить поиск видимости элемента с dynamic_model_id
        dynamic_element = xpath.find_visible(
            f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{dynamic_model_id}")]',
            timeout=3
        )
        self.logger.info(f'Элемент связи {dynamic_model_id} найден и отображается')

        return dynamic_model_id

    def delete_shape(self, model_id):
        xpath = XPathFinder(self.driver)
        action = ActionChains(self.driver)

        # Поиск основного элемента в SHAPES_TOOLS
        shape_tool_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES_TOOLS}/*[name()="g"][contains(@model-id, "{model_id}")]'
        shape_tool = xpath.find_visible(shape_tool_path, timeout=3)

        # Наведение курсора на найденный элемент
        self.hover_shape(model_id)

        # Поиск вложенного элемента (circle) внутри tools
        circle_tool_path = f'{WorkflowEditorLocators.WFEDITOR_SHAPES_TOOLS}/*[name()="g"][contains(@model-id, "{model_id}")]/*[name()="circle"]'
        circle_tool = xpath.find_visible(circle_tool_path, timeout=3)

        # Клик по найденному кругу
        action.move_to_element(circle_tool).click().perform()

        self.logger.info(f'Взаимодействие с инструментом фигуры {model_id} выполнено')

    def undo_redo_action(self, action, model_id, locator=True):
        """
        Выполняет 'Отменить' или 'Повторить' и проверяет изменение состояния элемента в DOM.

        :param driver: Экземпляр WebDriver.
        :param action: 'Отменить' или 'Повторить'.
        :param model_id: ID элемента в DOM.
        :param locator: Если True - ищет кнопку, если False - использует сочетание клавиш.
        """
        action = action.lower()
        self.logger.info(f"Выполнение действия: {action} для элемента с model_id: {model_id}")
        element_selector = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{model_id}")]'

        if action not in ["отменить", "повторить"]:
            raise ValueError("Действие должно быть 'Отменить' или 'Повторить'.")

        if locator:
            button_selector = f'{WorkflowEditorLocators.WFEDITOR_UNDOREDO}/a[contains(@title,"{action.capitalize()}")]/i'
            try:
                button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, button_selector)))
                button.click()
                self.logger.info(f"Клик по кнопке: {action.capitalize()}")
            except Exception as e:
                self.logger.error(f"Ошибка клика по кнопке: {e}")
        else:
            shortcut = Keys.CONTROL + 'z' if action == "отменить" else Keys.CONTROL + 'y'
            try:
                self.driver.switch_to.active_element.send_keys(shortcut)
                self.logger.info(f"Нажато сочетание клавиш: {shortcut}")
            except Exception as e:
                self.logger.error(f"Ошибка при нажатии сочетания клавиш: {e}")

        try:
            if action == "отменить":
                WebDriverWait(self.driver, 1).until(EC.invisibility_of_element_located((By.XPATH, element_selector)))
                self.logger.info(f"Элемент {model_id} успешно удалён!")
            else:
                WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, element_selector)))
                self.logger.info(f"Элемент {model_id} успешно восстановлен!")
        except:
            self.logger.error(f"Элемент {model_id} не изменил состояние после '{action}'!")

    def adjust_zoom_and_verify(self, attribute, model_id):
        """
        Получает текущее значение масштаба и размер элемента, изменяет масштаб,
        проверяет изменение размера и сравнивает с ожидаемым.

        :param driver: Экземпляр WebDriver.
        :param attribute: 'Отдалить' или 'Приблизить' или 'Автомасштаб'.
        :param model_id: ID модели элемента.
        """
        zoom_input_xpath = f'{WorkflowEditorLocators.WFEDITOR_ZOOM_INPUT}'
        element_selector = f'{WorkflowEditorLocators.WFEDITOR_SHAPES}/*[name()="g"][contains(@model-id, "{model_id}")]'

        # Получаем текущее значение масштаба перед изменением
        try:
            initial_zoom_value = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, zoom_input_xpath))).get_attribute("value")
            initial_zoom_percentage = int(initial_zoom_value.replace('%', ''))  # Преобразуем '125%' -> 125
            self.logger.info(f"Исходный масштаб перед изменением: {initial_zoom_percentage}%")
        except Exception as e:
            self.logger.error(f"Ошибка получения исходного масштаба: {e}")
            return False

        # Получаем исходный размер фигуры
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element_selector)))
            original_size = element.size
            self.logger.info(f"Исходный размер фигуры {model_id}: {original_size['width']}x{original_size['height']}")
        except Exception as e:
            self.logger.error(f"Ошибка получения исходного размера элемента {model_id}: {e}")
            return False

        # Нажимаем кнопку 'Отдалить' или 'Приблизить'
        zoom_button_xpath = f'{WorkflowEditorLocators.WFEDITOR_ZOOM}/a[contains(@title,"{attribute}")]'
        try:
            zoom_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, zoom_button_xpath)))
            zoom_button.click()
            self.logger.info(f"Нажата кнопка {attribute}")
        except Exception as e:
            self.logger.error(f"Ошибка клика по {attribute}: {e}")
            return False

        # Получаем новое значение масштаба после клика
        try:
            new_zoom_value = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, zoom_input_xpath))).get_attribute("value")
            new_zoom_percentage = int(new_zoom_value.replace('%', ''))  # Преобразуем '75%' -> 75
            self.logger.info(f"Текущий масштаб после изменения: {new_zoom_percentage}%")
        except Exception as e:
            self.logger.error(f"Ошибка получения нового масштаба: {e}")
            return False

        # Получаем новый размер фигуры после изменения масштаба
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element_selector)))
            new_size = element.size
            self.logger.info(f"Новый размер фигуры {model_id}: {new_size['width']}x{new_size['height']}")
        except Exception as e:
            self.logger.error(f"Ошибка получения нового размера элемента {model_id}: {e}")
            return False

        # Вычисляем, насколько изменился размер относительно начального масштаба
        expected_width = original_size['width'] * (new_zoom_percentage / initial_zoom_percentage)
        expected_height = original_size['height'] * (new_zoom_percentage / initial_zoom_percentage)

        if abs(new_size['width'] - expected_width) > 1 or abs(new_size['height'] - expected_height) > 1:
            self.logger.error(f"Ошибка: Размер фигуры {model_id} не изменился корректно!")
            return False

        self.logger.info(f"Масштаб успешно изменён, проверка пройдена!")
        return True
    
    def name_properties(self, name, action):
        """Метод для установки или проверки имени процесса/фигуры."""
        xpath = XPathFinder(self.driver)
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_NAME  # XPath до инпута имени
        check_xpath = f'{input_xpath}[@title="{name}"]'  # XPath для проверки имени
    
        if action == "set":
            self.logger.info(f"Устанавливаем имя: {name}")
            try:
                input_element = xpath.find_clickable(input_xpath, timeout=3)
                # Альтернативный метод очистки
                input_element.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
                input_element.send_keys(Keys.DELETE)  # Удалить
                input_element.send_keys(name)
                self.logger.info("Имя успешно установлено.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке имени: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем имя: {name}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Имя совпадает.")
                return True
            except Exception:
                self.logger.warning("Имя не совпадает.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def descriptions_properties(self, descriptions, action):
        """Метод для установки или проверки описания процесса/фигуры."""
        xpath = XPathFinder(self.driver)
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_DESCRIPTIONS  # XPath до `div`, содержащего `p`
        paragraph_xpath = f"{input_xpath}/p"  # XPath до самого текста
        name_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_NAME  # XPath до инпута имени названия

        if action == "set":
            self.logger.info(f"Устанавливаем описание: {descriptions}")
            try:
                input_element = xpath.find_clickable(input_xpath, timeout=3)
            
                # Очистка текущего содержимого
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)

                # Ввод нового описания
                input_element.send_keys(descriptions)

                self.logger.info("Описание успешно установлено.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке описания: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем описание: {descriptions}")
            try:
                actual_description = xpath.find_visible(paragraph_xpath, timeout=3).text  # Достаем текст `<p>`
                if actual_description.strip() == descriptions.strip():
                    self.logger.info("Описание совпадает.")
                    return True
                else:
                    self.logger.warning(f"Описание не совпадает: ожидалось '{descriptions}', получили '{actual_description}'")
                    return False
            except Exception:
                self.logger.warning("Описание не найдено.")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def term_properties(self, term, action):
        """Метод для установки или проверки срока процесса/фигуры."""
        xpath = XPathFinder(self.driver)
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_TERM  # XPath до инпута срока
        check_xpath = f'{input_xpath}[@title="{term}"]'  # XPath для проверки имени
    
        if action == "set":
            self.logger.info(f"Устанавливаем срок: {term}")
            try:
                input_element = xpath.find_clickable(input_xpath, timeout=3)
                # Альтернативный метод очистки
                input_element.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
                input_element.send_keys(Keys.DELETE)  # Удалить
                input_element.send_keys(term)
                self.logger.info("Срок успешно установлено.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке срока: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем срока: {term}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Срок совпадает.")
                return True
            except Exception:
                self.logger.warning("Срок не совпадает.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def notify_properties(self, period_notify, action):
        """Метод для установки или проверки периода уведомления."""
        xpath = XPathFinder(self.driver)
    
        # XPath до кнопки открытия выпадающего списка
        button_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_NOTIFY_TERM_BUTTON
        # XPath для поиска нужного элемента в списке
        list_xpath = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_NOTIFY_TERM_LIST}[text()="{period_notify}"]'
        # XPath для проверки значения в инпуте
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_NOTIFY_TERM_INPUT

        if action == "set":
            self.logger.info(f"Выбираем период уведомления: {period_notify}")
            try:
                # Открываем выпадающий список
                xpath.find_clickable(button_xpath, timeout=3).click()
                # Находим нужный элемент и кликаем
                xpath.find_located(list_xpath, timeout=3)
                self.logger.info(f"Строка {list_xpath} найдена в DOM")
                xpath.find_visible(list_xpath, timeout=3).click()
                self.logger.info("Период успешно установлен.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке периода: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем установленный период уведомления: {period_notify}")
            try:
                actual_notify_period = xpath.find_visible(input_xpath, timeout=3).get_attribute("title")
                if actual_notify_period == period_notify:
                    self.logger.info("Период совпадает.")
                    return True
                else:
                    self.logger.warning(f"Период не совпадает: ожидалось '{period_notify}', получили '{actual_notify_period}'")
                    return False
            except Exception:
                self.logger.warning("Период не найден.")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def role_properties(self, role_name, action, checkboxes, access_level=None, users=None):
        """Метод для создания или проверки роли процесса."""
        xpath = XPathFinder(self.driver)

        if action == "create":
            self.logger.info(f"Создаем роль: {role_name}")

            try:
                # Кликаем кнопку для создания роли
                element = xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_INSERT_ROLE, timeout=3).click()
            
                # Находим инпут для имени роли и вводим role_name
                self.logger.info(f'Задаем название роли - {role_name}')
                textarea_path = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_ROLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and @title="​"]/parent::div/following-sibling::div[contains(@class,"textarea")]/div/textarea'
                input_element = xpath.find_located(textarea_path, timeout=3)
                input_element.send_keys(role_name)
                input_element.send_keys(Keys.ENTER)
            
                # Ищем строку созданной роли
                new_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_ROLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and contains(@title, "{role_name}")]/parent::div/parent::td/parent::tr'
                xpath.find_visible(new_tr, timeout=3)

                # Выбираем уровень доступа
                self.logger.info(f'Выбираем уровень доступа - {access_level}')
                xpath.find_clickable(f'{new_tr}/td[@field=1]/div/span', timeout=3).click()
                xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_SHOW_LIST, timeout=3).click()
                xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_LIST}/td[contains(@title,"{access_level}")]', timeout=3).click()

                # Устанавливаем чекбоксы
                rows = xpath.find_located(WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_TRS, timeout=3, few=True)
                self.logger.info(f'Проставляем чекбоксы - {checkboxes.lower()}')
                self.logger.info(f"Найдено {len(rows)} строк чекбоксов")
                for index, row in enumerate(rows, start=1):  # Нумерация строк с 1
                    self.logger.info(f"Обрабатываем строку {index}: {row.text}")  

                    checkbox_xpath = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_TRS}[{index}]/td/div/span/i[contains(@class,"checkbox-{checkboxes.lower()}")]'
                    self.logger.info(f'Ищем чекбокс: {checkbox_xpath}')

                    try:
                        checkbox_element = xpath.find_visible(checkbox_xpath, timeout=0.1)
                    except Exception:
                        self.logger.info(f'Не нашли: {checkbox_xpath}')
                        checkbox_element = None

                    if not checkbox_element:
                        try:
                            icon_path = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_TRS}[{index}]/td/div/span/i'
                            self.logger.info(f'Ищем кнопку: {icon_path}')
                            checkbox_icon = xpath.find_clickable(icon_path, timeout=1)
                            checkbox_icon.click()
                        except Exception:
                            self.logger.warning(f'Не удалось кликнуть по чекбоксу в строке: {row}')
                            continue

                        try:
                            checkbox_element = xpath.find_visible(checkbox_xpath, timeout=2)
                            if checkbox_element:
                                self.logger.info(f'Чекбокс успешно изменен: {checkboxes.lower()}')
                            else:
                                self.logger.warning(f'Чекбокс не изменился после клика!')
                        except Exception:
                            self.logger.warning(f'Не удалось повторно найти чекбокс после клика!')

                xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_SHARE_READY, timeout=3).click()

                # Назначаем пользователей
                xpath.find_clickable(f'{new_tr}/td[@field=2]/div/span', timeout=3).click()
                input_users = xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_ROLE_CELLWITHDROPDOWN_INPUT, timeout=3)
                input_users.send_keys(USER1_LOGIN)
                xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_ROLE_CELLWITHDROPDOWN_DROPDOWN}[contains(@title,"{USER1_LOGIN}")]', timeout=3).click()
            
                self.logger.info("Роль успешно создана.")
            except Exception as e:
                self.logger.error(f"Ошибка при создании роли: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем роль: {role_name}")

            try:
                # Проверяем, что роль существует
                self.logger.info(f'Проверяем наличие роли: {role_name}')
                checking_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_ROLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and text()="{role_name}"]/parent::div/parent::td/parent::tr'
                xpath.find_visible(checking_tr, timeout=3, scroll=True)
                self.logger.info(f'Роль "{role_name}" найдена.')

                # Проверяем уровень доступа
                self.logger.info(f'Проверяем уровень доступа: {access_level}')
                check_access = f'{checking_tr}/td[@field=1]/div/span[contains(@title,"{access_level}")]'
                xpath.find_visible(check_access, timeout=3)
                self.logger.info(f'Уровень доступа "{access_level}" подтвержден.')

                # Проверяем пользователей
                self.logger.info(f'Проверяем наличие пользователя: {users}')
                check_users = f'{checking_tr}/td[@field=2]/div/span[contains(@title,"{", ".join(users)}")]'
                xpath.find_visible(check_users, timeout=3)
                self.logger.info(f'Пользователь "{users}" найден.')

                self.logger.info("Роль и доступы успешно проверены.")
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке роли: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'create' или 'check'")

    def observer_properties(self, action, role_name, users=None):
        xpath = XPathFinder(self.driver)
        self.logger.info(f'Начинаем обработку наблюдателя: {role_name}, action={action}, users={users}')

        if action == "add":
            try:
                self.logger.info("Ищем инпут и вводим название роли")
                observer_input = xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_OBSERVER_INPUT, timeout=3)
                observer_input.send_keys(role_name)

                self.logger.info("Ждём и нажимаем элемент выпадающего списка")
                observer_option = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_OBSERVER_LIST}[contains(@title,"{role_name}")]'
                xpath.find_clickable(observer_option, timeout=3).click()

                # Проверяем, что в таблице добавилась нужная строка
                actual_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_OBSERVER_TABLE}[contains(@title,"{role_name}")]/parent::div/parent::td/parent::tr'
                self.logger.info(f'Проверяем наличие строки наблюдателя: {actual_tr}')
                xpath.find_visible(actual_tr, timeout=3)
                self.logger.info(f'Наблюдатель "{role_name}" успешно добавлен.')

                # Если указан `users`, проверяем его наличие
                if users:
                    self.logger.info(f'Проверяем наличие пользователя: {users} по пути {actual_tr}/td//span[contains(@title,"{", ".join(users)}")]')
                    user_check = f'{actual_tr}/td//span[contains(@title,"{", ".join(users)}")]'
                    xpath.find_visible(user_check, timeout=3)
                    self.logger.info(f'Пользователь "{users}" подтвержден.')

            except Exception as e:
                self.logger.error(f"Ошибка при добавлении наблюдателя: {e}")
                raise

        elif action == "check":
            try:
                self.logger.info(f'Проверяем наличие наблюдателя: {role_name}')
                actual_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_OBSERVER_TABLE}[contains(@title,"{role_name}")]/parent::div/parent::td/parent::tr'
                self.logger.info(f'Ищем строку наблюдателя: {actual_tr}')
                xpath.find_visible(actual_tr, timeout=3)
                self.logger.info(f'Наблюдатель "{role_name}" найден.')

                # Если указан `users`, проверяем его наличие
                if users:
                    self.logger.info(f'Проверяем наличие пользователя: {users}')
                    user_check = f'{actual_tr}/td//span[contains(@title,"{", ".join(users)}")]'
                    self.logger.info(f'Ищем пользователя в строке: {user_check}')
                    xpath.find_visible(user_check, timeout=3)
                    self.logger.info(f'Пользователь "{users}" подтвержден.')

                return True

            except Exception as e:
                self.logger.error(f"Ошибка при проверке наблюдателя: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'add' или 'check'")

    def variables_properties(self, action, id, name, comment, type, content):
        xpath = XPathFinder(self.driver)

        if action == "add":
            self.logger.info(f'Начинаем добавление переменной: {id}')

            # Кликаем кнопку создания переменной
            self.logger.info("Кликаем кнопку создания переменной")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_INSERT_VARIABLE, timeout=3).click()

            # Вводим ID
            self.logger.info(f'Вводим ID: {id}')
            input_id = xpath.find_clickable(
                f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_VARIABLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and @title="​"]/parent::div/following-sibling::div/div[contains(@class,"box")]/input',
                timeout=3
            )
            input_id.send_keys(id)
            input_id.send_keys(Keys.ENTER)
            time.sleep(0.3)

            # Находим строку созданной переменной
            new_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_VARIABLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and contains(@title, "{id}")]/parent::div/parent::td/parent::tr'
            self.logger.info(f'Найдена строка переменной: {new_tr}')

            # Назначаем название
            self.logger.info(f'Назначаем название: {name}')
            xpath.find_clickable(f'{new_tr}/td[@field=1]', timeout=3).click()
            input_name = xpath.find_clickable(f'{new_tr}/td[@field=1]/div/div/textarea', timeout=3)
            input_name.send_keys(name)
            input_name.send_keys(Keys.ENTER)
            time.sleep(0.3)

            # Назначаем комментарий
            self.logger.info(f'Назначаем комментарий: {comment}')
            xpath.find_clickable(f'{new_tr}/td[@field=2]', timeout=3).click()
            input_comment = xpath.find_clickable(f'{new_tr}/td[@field=2]/div/div/textarea', timeout=3)
            input_comment.send_keys(comment)
            input_comment.send_keys(Keys.ENTER)
            time.sleep(0.3)

            # Выбираем тип
            self.logger.info(f'Выбираем тип переменной: {type}')
            xpath.find_clickable(f'{new_tr}/td[@field=3]', timeout=3).click()
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_VARIABLE_CELLWITHDROPDOWN_BUTTON, timeout=3).click()
            xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_VARIABLE_CELLWITHDROPDOWN_DROPDOWN}[text()="{type}"]', timeout=3).click()
            time.sleep(0.3)

            # Назначаем значение
            self.logger.info(f'Назначаем значение: {content}')
            xpath.find_clickable(f'{new_tr}/td[@field=4]', timeout=3).click()
            input_value = xpath.find_clickable(f'{new_tr}/td[@field=4]/div/div/textarea', timeout=3)
            input_value.send_keys(content)
            input_value.send_keys(Keys.ENTER)

            self.logger.info(f'Переменная "{id}" успешно добавлена.')

        elif action == "check":
            try:
                self.logger.info(f'Проверяем наличие переменной: {id}')
                checking_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_VARIABLE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and text()="{id}"]/parent::div/parent::td/parent::tr'
                xpath.find_visible(checking_tr, timeout=3, scroll=True)
                self.logger.info(f'Переменная "{id}" найдена.')

                # Проверяем наименование
                self.logger.info(f'Проверяем название переменной: {name}')
                check_name = f'{checking_tr}/td[@field=1]/div/span[contains(text(), "{name}")]'
                xpath.find_visible(check_name, timeout=3)
                self.logger.info(f'Название "{name}" подтверждено.')

                # Проверяем комментарий
                self.logger.info(f'Проверяем комментарий: {comment}')
                check_comment = f'{checking_tr}/td[@field=2]/div/span[contains(text(), "{comment}")]'
                xpath.find_visible(check_comment, timeout=3)
                self.logger.info(f'Комментарий "{comment}" подтвержден.')

                # Проверяем тип
                self.logger.info(f'Проверяем тип переменной: {type}')
                check_type = f'{checking_tr}/td[@field=3]/div/span[contains(text(), "{type}")]'
                xpath.find_visible(check_type, timeout=3)
                self.logger.info(f'Тип "{type}" подтвержден.')

                # Проверяем значение
                self.logger.info(f'Проверяем значение переменной: {content}')
                check_value = f'{checking_tr}/td[@field=4]/div/span[contains(text(), "{content}")]'
                xpath.find_visible(check_value, timeout=3)
                self.logger.info(f'Значение "{content}" подтверждено.')

                self.logger.info("Переменная успешно проверена.")
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке переменной: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'add' или 'check'")

    def stages_properties(self, action, name, number):
        xpath = XPathFinder(self.driver)

        if action == "add":
            self.logger.info(f'Добавляем стадию процесса: {name} (номер {number})')

            # Кликаем кнопку создания стадии
            self.logger.info("Кликаем кнопку создания стадии")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_INSERT_STAGE, timeout=3).click()

            # Назначаем название
            self.logger.info(f'Назначаем название стадии: {name}')
            input_name = xpath.find_clickable(f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGEE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and @title="​"]/parent::div/following-sibling::div[contains(@class,"textarea")]/div/textarea', timeout=3)
            input_name.send_keys(name)
            input_name.send_keys(Keys.ENTER)
            time.sleep(0.3)

            # Находим строку созданной стадии
            new_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGEE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and contains(@title, "{name}")]/parent::div/parent::td/parent::tr'
            self.logger.info(f'Найдена строка стадии: {new_tr}')

            # Назначаем номер стадии
            self.logger.info(f'Назначаем номер стадии: {number}')
            xpath.find_clickable(f'{new_tr}/td[@field=1]', timeout=3).click()
            input_number = xpath.find_clickable(f'{new_tr}/td[@field=1]/div/div/input', timeout=3)
            input_number.send_keys(number)
            input_number.send_keys(Keys.ENTER)

            self.logger.info(f'Стадия "{name}" успешно добавлена.')

        elif action == "check":
            try:
                self.logger.info(f'Проверяем наличие стадии: {name}')
                checking_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGEE_TRS}/td[contains(@class,"first")]/div/span[contains(@class,"text") and text()="{name}"]/parent::div/parent::td/parent::tr'
                xpath.find_visible(checking_tr, timeout=3, scroll=True)
                self.logger.info(f'Стадия "{name}" найдена.')

                # Проверяем номер стадии
                self.logger.info(f'Проверяем номер стадии: {number}')
                check_number = f'{checking_tr}/td[@field=1]/div/span[contains(text(), "{number}")]'
                xpath.find_visible(check_number, timeout=3)
                self.logger.info(f'Номер "{number}" подтвержден.')

                self.logger.info("Стадия успешно проверена.")
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке стадии: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'add' или 'check'")

    def automation_start(self, action_type, automation_type):
        xpath = XPathFinder(self.driver)
        self.logger.info(f'Начинаем обработку автоматизации при старте: {automation_type}')

        if action_type == "add":
            self.logger.info("Кликаем чекбокс 'Автоматизация при старте'")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_START_AUTO, timeout=3).click()

            self.logger.info("Открываем выпадающий список автоматизации")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_START_AUTO_FIRST_BUTTON, timeout=3).click()

            self.logger.info(f'Выбираем автоматизацию: {automation_type}')
            automation_option = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_START_AUTO_FIRST_lIST}[contains(@title,"{automation_type}")]'
            xpath.find_clickable(automation_option, timeout=3).click()

            self.logger.info(f'Автоматизация "{automation_type}" успешно добавлена.')

        elif action_type == "check":
            try:
                self.logger.info(f'Проверяем наличие автоматизации: {automation_type}')
                automation_input = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_START_AUTO_FIRST_INPUT}[contains(@title,"{automation_type}")]'
                xpath.find_visible(automation_input, timeout=3, scroll=True)
                self.logger.info(f'Автоматизация "{automation_type}" подтверждена.')
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке автоматизации: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action_type: {action_type}")
            raise ValueError("action_type должен быть 'add' или 'check'")

    def automation_finish(self, action_type, automation_type):
        xpath = XPathFinder(self.driver)
        self.logger.info(f'Начинаем обработку автоматизации при старте: {automation_type}')

        if action_type == "add":
            self.logger.info("Кликаем чекбокс 'Автоматизация при старте'")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_FINISH_AUTO, timeout=3).click()

            self.logger.info("Открываем выпадающий список автоматизации")
            xpath.find_clickable(WorkflowEditorLocators.WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_BUTTON, timeout=3).click()

            self.logger.info(f'Выбираем автоматизацию: {automation_type}')
            automation_option = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_lIST}[contains(@title,"{automation_type}")]'
            xpath.find_clickable(automation_option, timeout=3).click()

            self.logger.info(f'Автоматизация "{automation_type}" успешно добавлена.')

        elif action_type == "check":
            try:
                self.logger.info(f'Проверяем наличие автоматизации: {automation_type}')
                automation_input = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_INPUT}[contains(@title,"{automation_type}")]'
                xpath.find_visible(automation_input, timeout=3, scroll=True)
                self.logger.info(f'Автоматизация "{automation_type}" подтверждена.')
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке автоматизации: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action_type: {action_type}")
            raise ValueError("action_type должен быть 'add' или 'check'")

    def executor_properties(self, executor_name, action):
        """Метод для установки или проверки периода уведомления."""
        xpath = XPathFinder(self.driver)
    
        # XPath до кнопки открытия выпадающего списка
        button_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_EXECUTOR_BUTTON
        # XPath для поиска нужного элемента в списке
        list_xpath = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_EXECUTOR_LIST}[text()="{executor_name}"]'
        # XPath для проверки значения в инпуте
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_EXECUTOR_INPUT

        if action == "set":
            self.logger.info(f"Выбираем исполнителя: {executor_name}")
            try:
                # Открываем выпадающий список
                xpath.find_clickable(button_xpath, timeout=3).click()
                # Находим нужный элемент и кликаем
                xpath.find_located(list_xpath, timeout=3)
                xpath.find_visible(list_xpath, timeout=3).click()
                self.logger.info("Исполнитель успешно установлен.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке исполнителя: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем установленного исполнителя: {executor_name}")
            try:
                actual_executor = xpath.find_visible(input_xpath, timeout=3).get_attribute("title")
                if actual_executor == executor_name:
                    self.logger.info("Исполнитель совпадает.")
                    return True
                else:
                    self.logger.warning(f"Исполнитель не совпадает: ожидалось '{executor_name}', получили '{actual_executor}'")
                    return False
            except Exception:
                self.logger.warning("Исполнитель не найден.")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def shape_stages_properties(self, stage_name, action):
        """Метод для установки или проверки периода уведомления."""
        xpath = XPathFinder(self.driver)
    
        # XPath до кнопки открытия выпадающего списка
        button_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGE_BUTTON
        # XPath для поиска нужного элемента в списке
        list_xpath = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGE_LIST}[text()="{stage_name}"]'
        # XPath для проверки значения в инпуте
        input_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_STAGE_INPUT

        if action == "set":
            self.logger.info(f"Выбираем стадию: {stage_name}")
            try:
                # Открываем выпадающий список
                xpath.find_clickable(button_xpath, timeout=3).click()
                # Находим нужный элемент и кликаем
                xpath.find_located(list_xpath, timeout=3)
                xpath.find_visible(list_xpath, timeout=3).click()
                self.logger.info("Стадия успешно установлена.")
            except Exception as e:
                self.logger.error(f"Ошибка при установки стадии: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем установленную стадию: {stage_name}")
            try:
                actual_stage = xpath.find_visible(input_xpath, timeout=3).get_attribute("title")
                if actual_stage == stage_name:
                    self.logger.info("Стадия совпадает.")
                    return True
                else:
                    self.logger.warning(f"Стадия не совпадает: ожидалось '{stage_name}', получили '{actual_stage}'")
                    return False
            except Exception:
                self.logger.warning("Стадия не найдена.")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def connections_properties(self, action, target_element,trans_name, result):
        """Метод для проверки таблицы связей фигуры."""
        xpath = XPathFinder(self.driver)
        actual_tr = f'{WorkflowEditorLocators.WFEDITOR_PROPERTIES_CONNECT_TRS}//span[contains(@title,"{target_element}")]/ancestor::tr[1]'

        if action == "set":
            self.logger.info(f"Ищем строку с целевым элементом: {target_element}")

            try:
                # Ищем актуальную строку
                xpath.find_visible(actual_tr, timeout=3)

                # Вводим наименование перехода
                self.logger.info(f'Вводим наименование перехода - {trans_name}')
                xpath.find_clickable(f'{actual_tr}/td[@field=1]/div/span', timeout=3).click()
                input_name = xpath.find_clickable(f'{actual_tr}/td[@field=1]/div/div/textarea', timeout=3)
                input_name.send_keys(trans_name)
                input_name.send_keys(Keys.ENTER)
                time.sleep(0.3)

                # Вводим результат
                xpath.find_clickable(f'{actual_tr}/td[@field=2]/div/span', timeout=3).click()
                input_result = xpath.find_clickable(f'{actual_tr}/td[@field=2]/div/div/input', timeout=3)
                input_result.send_keys(result)
                input_result.send_keys(Keys.ENTER)
            
                self.logger.info("Связь фигуры успешно настроена.")
            except Exception as e:
                self.logger.error(f"Ошибка при настройки связи фигуры: {e}")
                raise

        elif action == "check":
            self.logger.info(f"Проверяем связь с целевым элементом: {target_element}")

            try:
                # Ищем актуальную строку
                xpath.find_visible(actual_tr, timeout=3)

                # Проверяем наименование перехода
                self.logger.info(f'Проверяем уровень доступа: {trans_name}')
                check_trans = f'{actual_tr}/td[@field=1]/div/span[contains(text(), "{trans_name}")]'
                xpath.find_visible(check_trans, timeout=3)
                self.logger.info(f'Название перехода "{check_trans}" подтверждено.')

                # Проверяем результат
                self.logger.info(f'Проверяем результат: {result}')
                check_result = f'{actual_tr}/td[@field=2]/div/span[contains(text(), "{result}")]'
                xpath.find_visible(check_result, timeout=3)
                self.logger.info(f'Результат "{check_result}" подтвержден.')

                self.logger.info("Параметры связи успешно проверены.")
                return True

            except Exception as e:
                self.logger.warning(f"Ошибка при проверке связи: {e}")
                return False

        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def shape_exit_result_properties(self, action, content):
        """Метод для установки или проверки результата выхода из фигуры."""
        xpath = XPathFinder(self.driver)

        exit_element = WorkflowEditorLocators.WFEDITOR_PROPERTIES_EXIT_RESULT
        status_map = {
            "null": f'{exit_element}[contains(@class,"svg-circle-24")]',
            "success": f'{exit_element}[contains(@class,"svg-check-circle-24")]',
            "fail": f'{exit_element}[contains(@class,"svg-cancel-circle-24")]'
        }

        if action == "set":
            self.logger.info(f"Устанавливаем результат выхода: {content}")

            # Определяем текущий статус как ключ, а не XPath
            current_status_key = next((key for key, status in status_map.items() if xpath.find_visible(status)), None)
            self.logger.info(f"Текущий статус перед изменением: {current_status_key}")

            if current_status_key == content:
                self.logger.info(f"Статус уже '{content}', клик не требуется")
                return

            # Определяем количество кликов для изменения статуса
            click_count = {
                ("null", "success"): 1,
                ("null", "fail"): 2,
                ("success", "fail"): 1,
                ("fail", "null"): 1
            }.get((current_status_key, content), None)

            self.logger.info(f"click_count определен как: {click_count}")

            if click_count:
                self.logger.info(f"Текущий статус: {current_status_key}, кликов потребуется: {click_count}")
                try:
                    for _ in range(click_count):
                        element = xpath.find_clickable(exit_element)
                        element.click()
                        time.sleep(0.1)
                    xpath.find_located(status_map[content])
                    self.logger.info(f"Результат выхода установлен в '{content}'")
                except Exception as e:
                    self.logger.error(f"Ошибка при клике: {e}")

        elif action == "check":
            self.logger.info(f"Проверяем результат выхода: {content}")
            if xpath.find_visible(status_map[content]):
                self.logger.info(f"Статус соответствует: {content}")
                return True
            else:
                self.logger.warning(f"Ожидался статус '{content}', но он не соответствует")
                return False

    def special_check_url(self):
        '''Метод предназначени только для специфического кейса проверки скопированной ссылки на процесс и ссылки в url'''
        xpath = XPathFinder(self.driver)
        input_description_xpath = WorkflowEditorLocators.WFEDITOR_PROPERTIES_DESCRIPTIONS
        # Вставка скопированной ссылки процесса в поле "Описание"
        element = xpath.find_clickable(input_description_xpath, timeout=3)
        element.click()
        element.send_keys(Keys.CONTROL, 'v')
        # Получение текущего URL в переменную
        current_url = self.driver.current_url
        self.logger.info(f"Текущий URL вкладки: {current_url}")

        check_description_xpath = f'{input_description_xpath}/p[contains(text(),"{current_url}")]'
        if xpath.find_located(check_description_xpath, timeout=3):
            self.logger.info(f"Скопированная ссылка процесса соответствует текущему URL: {current_url}")
            return True
        else:
            self.logger.warning(f"Скопированная ссылка процесса не соответствует текущему URL: {current_url}")
            return False  