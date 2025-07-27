import time
from venv import logger
from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.my_tasks_locators import MyTasksLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.my_files_editor_locators import MyFilesEditorLocators
from locators.base_locators import BaseLocators  # Общие локаторы, которые могут использоваться на разных страницах
from utils.element_searching import XPathFinder
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# Импорт менеджера загрузок для проверки скачивания файлов
from utils.download_manager import DownloadManager

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
        time.sleep(0.5)  # Ждем, для стабильности 
        input_element.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_element.send_keys(Keys.DELETE)  # Удалить выделенное
        time.sleep(0.5)  # Ждем, для стабильности
        input_element.send_keys(process_name)
        self.logger.info(f"Имя процесса '{process_name}' введено в поле типа задачи")
        try:
            match = xpath.find_clickable(f'{MyTasksLocators.MY_TASKS_TASK_TYPE_TRS}[contains(@title,"{process_name}")]', timeout=3)
        except TimeoutException:
            match = None
        time.sleep(1)  # Ждем, для стабильности
        if match:
            self.logger.info(f"Процесс '{process_name}' найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return True
        else:
            self.logger.info(f"Процесс '{process_name}' не найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return False

    def create_task(self, task_name, task_description=None, task_type=None, deadline=None, executor=None, executors=None, executors_massive=None, attache_file=None, from_file=False):
        """Создание задачи:
        task_name - имя задачи
        task_description - описание задачи
        task_type - тип задачи (используемый маршрут)
        deadline - дедлайн выполнения задачи
        executor - Исполнитель задачи
        executors - Массив вида [("Название роли1","Логин1"),("Название роли2","Логин2")]
        executors_massive - Массив вида [("Логин1","Уровень доступа1"),("Логин2","Уровень доступа2")]
        attache_file - название файла, который необходимо прикрепить к задаче
        from_file - чекбокс указывающий на то, что задача будет создана из файла, если false из раздела 'Мои задачи'"""
        if not from_file:
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_CREATE_TASK_BUTTON, timeout=3).click()
        else:
            self.xpath.find_clickable(MyFilesEditorLocators.SEND_FOR_APPROVAL_BUTTON, timeout=3).click()
        input_name = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_NAME_INPUT, timeout=3)
        input_name.click()  # Кликаем по полю ввода названия задачи
        input_name.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_name.send_keys(Keys.DELETE)  # Удалить
        input_name.send_keys(task_name)
        self.logger.info("Название задачи успешно установлено.")

        if task_description:
            if not from_file:
                input_description = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_DESCRIPTION_INPUT, timeout=3)
            else:
                input_description = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_FROM_FILE_TASK_DESCRIPTION_INPUT, timeout=3)
            input_description.click()  # Кликаем по полю ввода описания задачи
            input_description.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_description.send_keys(Keys.DELETE)  # Удалить
            input_description.send_keys(task_description)
            self.logger.info("Описание задачи успешно установлено.")

        if task_type:
            if not from_file:
                succes_path = f'{MyTasksLocators.MY_TASKS_TASK_TYPE_TRS}[contains(@title,"{task_type}")]/ancestor::tr'
                input_type = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_TYPE_INPUT, timeout=5)
            else:
                succes_path = f'{MyTasksLocators.MY_TASKS_FROM_FILE_TASK_TYPE_TRS}[contains(@title,"{task_type}")]/ancestor::tr'
                input_type = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_FROM_FILE_TASK_TYPE_INPUT, timeout=5)
            input_type.click()
            input_type.send_keys(Keys.CONTROL + "a")
            input_type.send_keys(" ")
            input_type.send_keys(Keys.DELETE)
            if task_type not in ["Параллельное согласование", "Последовательное согласование"]:
                input_type.send_keys(task_type)
                self.logger.info(f"Имя процесса '{task_type}' введено в поле типа задачи")
            else:
                self.logger.info(f"Исключение, не вводим, т.к. поиск не сработает")
            time.sleep(0.5) # Ждем, для стабильности
            self.xpath.find_clickable(succes_path, timeout=3).click()
            self.logger.info(f"Процесс '{task_type}' найден в списке типов задач и выбран")

        if deadline:
            input_deadline = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_DEADLINE_INPUT, timeout=3)
            input_deadline.click()  # Кликаем по полю ввода описания задачи
            input_deadline.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_deadline.send_keys(Keys.DELETE)  # Удалить
            input_deadline.send_keys(deadline)
            self.logger.info("Дедлайн задачи успешно установлен.")

        if executor:
            input_executor = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_PERFORMER_INPUT, timeout=3)
            input_executor.click()
            input_executor.send_keys(Keys.CONTROL + "a")
            input_executor.send_keys(Keys.DELETE)
            input_executor.send_keys(executor)
            self.logger.info(f"Исполнитель задачи '{executor}' успешно введен в поле исполнителя задачи.")
            succes_path = f'{MyTasksLocators.MY_TASKS_TASK_PERFORMER_TRS}[contains(@title,"{executor}")]'
            time.sleep(0.5)  # Ждем, для стабильности
            self.xpath.find_clickable(succes_path, timeout=3).click()
            self.logger.info(f"Пользователь '{executor}' найден в списке исполнителей задач")

        if executors:
            # ИЗВЛЕКАЕМ ЗАНЧЕНИЯ ИЗ МАССИВА ВИДА Массив вида [("Название роли1","Логин1"),("Название роли2","Логин2")]
            for role_name, login in executors:
                input_xpath = f'{MyTasksLocators.MY_TASKS_TASK_ROLE}[contains(@title,"{role_name}")]/parent::div/div/input'
                input_element = self.xpath.find_clickable(input_xpath, timeout=3)
                input_element.click()  # Кликаем по полю ввода роли
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys(login)
                self.logger.info(f"Логин {login} успешно введен в инпут роли '{role_name}'")
                time.sleep(0.5)  # Ждем, для стабильности
                succes_xpath = f'{MyTasksLocators.MY_TASKS_TASK_ROLE}/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[2]//span[contains(@title,"{login}")]'
                self.xpath.find_clickable(succes_xpath, timeout=3).click()
                self.logger.info(f"Роль '{role_name}' с логином '{login}' успешно введена в поле исполнителя задачи.")

        if executors_massive:
            for executor, access_level in executors_massive:
                input_executor = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_PERFORMER_INPUT, timeout=3)
                input_executor.click()
                input_executor.send_keys(Keys.CONTROL + "a")
                input_executor.send_keys(Keys.DELETE)
                input_executor.send_keys(executor)
                self.logger.info(f"Исполнитель задачи '{executor}' успешно введен в поле исполнителя задачи.")

                succes_path = f'{MyTasksLocators.MY_TASKS_TASK_PERFORMER_TRS}[contains(@title,"{executor}")]'
                time.sleep(0.5)  # Ждем, для стабильности
                self.xpath.find_clickable(succes_path, timeout=3).click()
                self.logger.info(f"Пользователь '{executor}' найден в списке исполнителей задач")

                current_tr = self.xpath.find_located(f'{MyTasksLocators.MY_TASKS_TASK_ACTORS_TRS}/td[contains(@class,"string")]/div/span[@title="{executor}"]/ancestor::tr')
                self.logger.info(f"Найдена текущая строка исполнителя")
                access_trigger = current_tr.find_element(By.XPATH, './td[contains(@class,"int")and not(contains(@class,"first"))]')
                self.logger.info(f"Найдена текущая строка доступа исполнителя")
                access_trigger.click()
                self.logger.info(f"Клик по триггеру доступа исполнителя")
                time.sleep(0.5) # Ждем, для стабильности
                access_trigger.click()
                self.logger.info(f"Клик по триггеру доступа исполнителя (второй раз, чтобы открыть список уровней доступа)")

                share_trigger = current_tr.find_element(By.XPATH, MyTasksLocators.MY_TASKS_TASK_ACCESS_TRIGGER)
                share_trigger.click()

                level_elements = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, MyTasksLocators.MY_TASKS_TASK_ACCESS_LEVELS))
                )

                for level in level_elements:
                    if level.get_attribute("title") == access_level:
                        level.click()
                        break
       
        if attache_file:
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_DOCUMENTS_TAB, timeout=3).click()
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_DOCUMENTS_ADD_BUTTON, timeout=3).click()
            search_file_by_name = f'{MyTasksLocators.MY_TASKS_DOCUMENTS_ADD_FILE_TD}[contains(@title,"{attache_file}")]'
            element = self.xpath.find_visible(search_file_by_name, timeout=3)
            ActionChains(self.driver).move_to_element(element).perform()
            checkbox = f'{search_file_by_name}/ancestor::tr/td[contains(@class,"check")]//i'
            self.xpath.find_clickable(checkbox, timeout=3).click()
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_DOCUMENTS_ADD_FILE_SELECT_BUTTON, timeout=3).click()
            self.logger.info(f"Файл '{attache_file}' успешно прикреплен к задаче.")

        if not from_file:
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_CREATE_BUTTON).click()
        else:
            self.xpath.find_clickable(MyTasksLocators.MY_TASKS_SEND_FOR_APPROVAL_BUTTON).click()

        self.close_all_windows()
        self.logger.info("Задача успешно создана.")

    def create_subtask(self, subtask_name, task_description=None, deadline=None, executor=None):

        self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CREATE_SUBTASK_BUTTON, timeout=3).click()
        
        input_name = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_NAME_INPUT, timeout=3)
        input_name.click()  # Кликаем по полю ввода названия задачи
        input_name.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_name.send_keys(Keys.DELETE)  # Удалить
        input_name.send_keys(subtask_name)
        self.logger.info("Название задачи успешно установлено.")

        if task_description:
            input_description = self.wait_and_fill_contenteditable(MyTasksLocators.MY_TASKS_TASK_DESCRIPTION_INPUT, timeout=3)
            input_description.click()  # Кликаем по полю ввода описания задачи
            input_description.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_description.send_keys(Keys.DELETE)  # Удалить
            input_description.send_keys(task_description)
            self.logger.info("Описание задачи успешно установлено.")

        if deadline:
            input_deadline = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_DEADLINE_INPUT, timeout=3)
            input_deadline.click()  # Кликаем по полю ввода описания задачи
            input_deadline.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_deadline.send_keys(Keys.DELETE)  # Удалить
            input_deadline.send_keys(deadline)
            self.logger.info("Дедлайн задачи успешно установлен.")

        if executor:
            input_executor = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_PERFORMER_INPUT, timeout=3)
            input_executor.click()
            input_executor.send_keys(Keys.CONTROL + "a")
            input_executor.send_keys(Keys.DELETE)
            input_executor.send_keys(executor)
            self.logger.info(f"Исполнитель задачи '{executor}' успешно введен в поле исполнителя задачи.")
            succes_path = f'{MyTasksLocators.MY_TASKS_TASK_PERFORMER_TRS}[contains(@title,"{executor}")]'
            if self.xpath.find_clickable(succes_path, timeout=3):
                self.logger.info(f"Пользователь '{executor}' найден в списке исполнителей задач")
                self.xpath.find_clickable(succes_path, timeout=3).click()
            else:
                self.logger.error(f"Пользователь '{executor}' не найден в списке исполнителей задач")

        self.xpath.find_clickable(MyTasksLocators.MY_TASKS_CREATE_BUTTON).click()
        self.close_all_windows()
        self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
        self.logger.info("Подзадача успешно создана.")

    def right_click_and_select_action(self, object_name, action_name, max_retries=5):
        """Находит процесс по имени, кликает ПКМ и выбирает действие из выпадающего списка, 
        обеспечивая устойчивость к изменениям DOM."""
        xpath = XPathFinder(self.driver)
    
        target_xpath = f'{MyTasksLocators.MY_TASKS_LIST}/span[@title="{object_name}"]'
        action_xpath = f'{MyTasksLocators.MY_TASKS_DROPDOWN}/td[@title="{action_name}"]'

        for attempt in range(max_retries):
            try:
                # Перепроверяем список элементов и ищем процесс
                process_element = xpath.find_located(target_xpath, timeout=10, few=False)

                if process_element:
                    self.logger.info(f"Попытка {attempt + 1}: Процесс '{object_name}' найден.")

                    # Скроллим до элемента
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", process_element)

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
                    time.sleep(1)  # Ждем, чтобы форма успела загрузиться
                    return True

            except StaleElementReferenceException:
                self.logger.warning(f"Элемент '{object_name}' устарел, пробуем заново...")
                time.sleep(1)  # Ждем, чтобы дать DOM перестроиться

        self.logger.error(f"Не удалось выполнить действие '{action_name}' для '{object_name}' после {max_retries} попыток.")
        return False

    def task_name_properties(self, name, action):
        """Метод для установки или проверки имени задачи."""
        xpath = XPathFinder(self.driver)
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_TITLE_INPUT  # XPath до инпута имени
        check_xpath = f'{input_xpath}[@title="{name}"]'  # XPath для проверки имени
    
        if action == "set":
            self.logger.info(f"Устанавливаем имя: {name}")
            try:
                input_element = xpath.find_clickable(input_xpath, timeout=3)
                input_element.click()
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

    def task_deadline_properties(self, deadline, action):
        """Метод для установки или проверки дедлайна задачи."""
        xpath = XPathFinder(self.driver)
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_DEADLINE_INPUT
        check_xpath = f'{input_xpath}[@title="{deadline}"]'

        if action == "set":
            self.logger.info(f"Устанавливаем дедлайн: {deadline}")
            try:
                input_element = xpath.find_visible(input_xpath, timeout=3)
                input_element.click()
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys(deadline)
                input_element.send_keys(Keys.ENTER)
                xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CALENDAR_ACTIVE_DATE, timeout=3).click()
                time.sleep(1)  # Ждем, чтобы дата была установлена
                self.logger.info("Дедлайн успешно установлен.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке дедлайна: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем дедлайн: {deadline}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Дедлайн совпадает.")
                return True
            except Exception:
                self.logger.warning("Дедлайн не совпадает.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def task_description_properties(self, description, action):
        """Метод для установки или проверки описания задачи."""
        xpath = XPathFinder(self.driver)
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_DESCRIPTION_INPUT
        check_xpath = f'{input_xpath}/p[text()="{description}"]'

        if action == "set":
            self.logger.info(f"Устанавливаем описание: {description}")
            try:
                input_element = xpath.find_visible(input_xpath, timeout=3)
                input_element.click()
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys(description)
                time.sleep(1)  # Ждем, чтобы дата была установлена
                self.logger.info("Описание успешно установлено.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке описания: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем описание: {description}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Описание совпадает.")
                return True
            except Exception:
                self.logger.warning("Описание не совпадает.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def task_executor_properties(self, executor_login, action):
        """Метод для установки или проверки исполнителя задачи."""
        xpath = XPathFinder(self.driver)
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_EXECUTOR_INPUT
        select_xpath = f'{MyTasksLocators.MY_TASKS_TASKFORM_EXECUTOR_TRS}//ancestor::tr'
        check_xpath = f'{input_xpath}[@title="{executor_login}"]'

        if action == "set":
            self.logger.info(f"Устанавливаем исполнителя: {executor_login}")
            try:
                input_element = xpath.find_visible(input_xpath, timeout=3)
                input_element.click()
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys(executor_login)
                xpath.find_clickable(select_xpath, timeout=3).click()
                self.close_all_windows()
                self.logger.info("Исполнитель успешно установлен.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке исполнителя: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем исполнителя: {executor_login}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Исполнитель совпадает.")
                return True
            except Exception:
                self.logger.warning("Исполнитель не совпадает.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def task_oberver_properties(self, observer_login):
        """Метод по добавлению наблюдателя в открытый taskform задачи."""
        self.logger.info(f"Начинаем добавление наблюдателя: {observer_login}")

        observe_button_xpath = MyTasksLocators.MY_TASKS_TASKFORM_WATCH_BUTTON
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_WATCHER_INPUT
        add_observers_target_tr_xpath = f'{MyTasksLocators.MY_TASKS_TASKFORM_ADD_WATCHER_TRS}[contains(@title,"{observer_login}")]/ancestor::tr'
        observers_target_tr_xpath = f'{MyTasksLocators.MY_TASKS_TASKFORM_WATCHERS_LIST}[@title="{observer_login}"]'

        self.xpath.find_clickable(observe_button_xpath, timeout=3).click()

        input_element = self.xpath.find_clickable(input_xpath, timeout=3)
        input_element.click()
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.DELETE)
        input_element.send_keys(observer_login)

        self.logger.info(f"Выбираем наблюдателя '{observer_login}' из выпадающего списка")
        self.xpath.find_clickable(add_observers_target_tr_xpath, timeout=3).click()

        self.logger.info("Проверяем, что наблюдатель появился в списке")
        self.xpath.find_visible(observers_target_tr_xpath, timeout=3)

        self.logger.info(f"Наблюдатель '{observer_login}' успешно добавлен в задачу")
    
    def check_access_to_task_fields(self, fields_massive):
        """
        Проверяет доступность редактирования полей в taskform.
        Если поле указано в fields_massive — ожидается, что оно кликабельно.
        Если не указано — ожидается, что оно НЕ кликабельно.
        """
        self.logger.info(f"Запущена проверка доступа к полям: {fields_massive}")
        timeout = 1

        # Обычные поля
        all_fields = {
            "Название": MyTasksLocators.MY_TASKS_TASKFORM_TITLE_INPUT,
            "Исполнитель": MyTasksLocators.MY_TASKS_TASKFORM_EXECUTOR_INPUT,
            "Дедлайн": MyTasksLocators.MY_TASKS_TASKFORM_DEADLINE_INPUT,
            "Описание": MyTasksLocators.MY_TASKS_TASKFORM_DESCRIPTION_INPUT,
        }

        for field_name, xpath in all_fields.items():
            should_be_clickable = field_name in fields_massive
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                if should_be_clickable:
                    self.logger.info(f"Поле '{field_name}' доступно, как ожидалось.")
                else:
                    self.logger.error(f"Поле '{field_name}' доступно, хотя не должно быть.")
                    return False
            except Exception as e:
                if should_be_clickable:
                    self.logger.error(f"Поле '{field_name}' недоступно, хотя должно быть: {e}")
                    return False
                else:
                    self.logger.info(f"Поле '{field_name}' недоступно, как ожидалось.")

        # Наблюдатели
        try:
            self.driver.find_element(By.XPATH, MyTasksLocators.MY_TASKS_TASKFORM_WATCH_BUTTON).click()
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, MyTasksLocators.MY_TASKS_TASKFORM_WATCHER_INPUT))
            )
            if "Наблюдатели" in fields_massive:
                self.logger.info("Поле 'Наблюдатели' доступно, как ожидалось.")
            else:
                self.logger.error("Поле 'Наблюдатели' доступно, хотя не должно быть.")
                return False
        except Exception as e:
            if "Наблюдатели" in fields_massive:
                self.logger.error(f"Поле 'Наблюдатели' недоступно, хотя должно быть: {e}")
                return False
            else:
                self.logger.info("Поле 'Наблюдатели' недоступно, как ожидалось.")
        finally:
            try:
                self.driver.find_element(By.XPATH, MyTasksLocators.MY_TASKS_TASKFORM_WATCH_BUTTON).click()
            except:
                pass

        # Кастомные кнопки, кли кабельность которых не может отследить селениум
        custom_buttons = {
            "Создание подзадачи": (
                MyTasksLocators.MY_TASKS_TASKFORM_CREATE_SUBTASK_BUTTON,
                f'{MyTasksLocators.MY_TASKS_TASKFORM_CREATE_SUBTASK_BUTTON}[contains(@class,"disabled")]'
            ),
            "Управление файлами": [
                (
                    MyTasksLocators.MY_TASKS_TASKFORM_ADD_FILE_BUTTON,
                    f'{MyTasksLocators.MY_TASKS_TASKFORM_ADD_FILE_BUTTON}[contains(@class,"disabled")]'
                ),
                (
                    MyTasksLocators.MY_TASKS_TASKFORM_DELETE_FILE_BUTTON,
                    f'{MyTasksLocators.MY_TASKS_TASKFORM_DELETE_FILE_BUTTON}[contains(@class,"disabled")]'
                )
            ]
        }

        for field_name, locators in custom_buttons.items():
            should_be_clickable = field_name in fields_massive
            try:
                if isinstance(locators, list):
                    for enabled_xpath, disabled_xpath in locators:
                        xpath = enabled_xpath if should_be_clickable else disabled_xpath
                        self.driver.find_element(By.XPATH, xpath)
                else:
                    enabled_xpath, disabled_xpath = locators
                    xpath = enabled_xpath if should_be_clickable else disabled_xpath
                    self.driver.find_element(By.XPATH, xpath)

                self.logger.info(f"Кнопка '{field_name}' в ожидаемом состоянии.")
            except Exception as e:
                self.logger.error(f"Кнопка '{field_name}' не в ожидаемом состоянии: {e}")
                return False

        self.logger.info("Проверка доступа к полям завершена успешно.")
        return True
    
    def task_comment_properties(self, comment_text, action):
        """Метод для установки или проверки комментария к задаче."""
        xpath = XPathFinder(self.driver)
        click_xpath = MyTasksLocators.MY_TASKS_TASKFORM_ADD_COMMENT_BUTTON
        input_xpath = MyTasksLocators.MY_TASKS_TASKFORM_COMMENT_TEXTAREA
        save_xpath = MyTasksLocators.MY_TASKS_TASKFORM_COMMENT_SAVE_BUTTON
        check_xpath = f'{MyTasksLocators.MY_TASKS_TASKFORM_COMMENT_LIST}[text()="{comment_text}"]'

        if action == "set":
            self.logger.info(f"Устанавливаем комментарий: {comment_text}")
            try:
                click_element = xpath.find_visible(click_xpath, timeout=3)
                click_element.click()
                input_element = xpath.find_visible(input_xpath, timeout=3)
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys(comment_text)
                time.sleep(0.5)  # Ждем, для стабильности
                xpath.find_clickable(save_xpath, timeout=3).click()
                self.logger.info("Комментарий успешно добавлен.")
            except Exception as e:
                self.logger.error(f"Ошибка при установке комментария: {e}")
                raise
        elif action == "check":
            self.logger.info(f"Проверяем комментарий: {comment_text}")
            try:
                xpath.find_visible(check_xpath, timeout=3)
                self.logger.info("Комментарий найден.")
                return True
            except Exception:
                self.logger.warning("Комментарий не найден.")
                return False
        else:
            self.logger.error(f"Недопустимое значение action: {action}")
            raise ValueError("action должен быть 'set' или 'check'")

    def download_history_task(self, task_name, format_name):
        '''Метод проверяет успешное скачивания истории таска в указанном формате'''
        xpath = XPathFinder(self.driver)
        dropdown_button = MyTasksLocators.MY_TASKS_TASKFORM_DOWNLOAD_HISTORY_BUTTON
        download_by_format = f'{MyTasksLocators.MY_TASKS_TASKFORM_DOWNLOAD_HISTORY_FORMATS_LIST}[contains(@title,"{format_name}")]'
        download_manager = DownloadManager()

        self.logger.info(
            f"Начало проверки скачивания истории задачи '{task_name}' в формате '{format_name}'")
        xpath.find_clickable(dropdown_button, timeout=3).click()
        xpath.find_clickable(download_by_format, timeout=3).click()
        download_manager.verify_downloaded_file(f"История согласования '{task_name}'.{format_name}")
        self.logger.info(
            f"Файл 'История согласования {task_name}.{format_name}' успешно загружен!")

    def open_subtask(self, task_name, subtask_massive):
        '''Метод октрывает подзадачу внутри основной задачи'''
        # Ищем основной tr по task_name
        xpath = XPathFinder(self.driver)
        target_span_xpath = f'{MyTasksLocators.MY_TASKS_LIST}/span[@title="{task_name}"]'

        for i, (position, subtask_name) in enumerate(subtask_massive):
            try:
                # Получаем tr на указанной позиции после основной
                indexed_tr_xpath = f"{target_span_xpath}/ancestor::tr/following-sibling::tr[{position}]"

                # Ищем span внутри этого tr и открываем таск кликом
                xpath.find_clickable(f'{indexed_tr_xpath}//span[@title="{subtask_name}"]', timeout=3).click()
                self.logger.info(f"Найдена и октрыта подзадача '{subtask_name}' на позиции {position}")
                time.sleep(1)  # Ждем, чтобы форма успела загрузиться
            except Exception as e:
                self.logger.error(f"Ошибка при октрытии подзадачи '{subtask_name}' на позиция {position}) от {task_name}: {e}")
                raise

    def complete_task(self, task_name: str, subtask_massive: list, waiting=True):
        # Ищем основной tr по task_name
        xpath = XPathFinder(self.driver)
        target_span_xpath = f'{MyTasksLocators.MY_TASKS_LIST}/span[@title="{task_name}"]'

        for i, (position, subtask_name, action) in enumerate(subtask_massive):
            try:
                # Получаем tr на указанной позиции после основной
                indexed_tr_xpath = f"{target_span_xpath}/ancestor::tr/following-sibling::tr[{position}]"

                # Ищем span внутри этого tr и открываем таск кликом
                xpath.find_clickable(f'{indexed_tr_xpath}//span[@title="{subtask_name}"]', timeout=3).click()
                self.logger.info(f"Найдена подзадача '{subtask_name}' на позиции {position}")

                # Ждём, чтобы форма открылась и клкиаем по кнопке действий
                actions_btn = xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_ACTIONS_BUTTON, timeout=3)
                time.sleep(1)
                actions_btn.click()

                # Выбираем и нажимаем действие из выпадающего списка и закрываем taskform
                xpath.find_clickable(f'{MyTasksLocators.MY_TASKS_TASKFORM_ACTIONS_DROPDOWN}//td[contains(@title,"{action}")]', timeout=3).click()
                time.sleep(2)  # Ждем, чтобы форма успела закрыться
                self.logger.info(f"Подзадача '{subtask_name}' на позиции {position} успешно завершена с действием '{action}'")
                # Ждём уведомления о выполнении действия с задачей
                if waiting:
                    self.close_all_windows()
                # Закрываем форму задачи для всех, кроме последней подзадачи
                if i < len(subtask_massive) - 1:
                    xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()

            except Exception as e:
                self.logger.warning(f"Ошибка при обработке подзадачи '{subtask_name}' действием '{action}' на позиция {position}): {e}")
                raise

    def complete_simple_task(self, task_name: str, action: str):
        # Ищем tr по task_name
        xpath = XPathFinder(self.driver)
        target_span_xpath = f'{MyTasksLocators.MY_TASKS_LIST}/span[@title="{task_name}"]'
        xpath.find_clickable(target_span_xpath, timeout=3).click()

        # Ждём, чтобы форма открылась и клкиаем по кнопке действий
        actions_btn = xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_ACTIONS_BUTTON, timeout=3)
        time.sleep(1)
        actions_btn.click()

        # Выбираем и нажимаем действие из выпадающего списка и кликаем
        xpath.find_clickable(f'{MyTasksLocators.MY_TASKS_TASKFORM_ACTIONS_DROPDOWN}//td[contains(@title,"{action}")]', timeout=3).click()
        # Ждём уведомления о выполнении действия с задачей
        self.close_all_windows()
        self.logger.info(f"Действие {action} выполнено для {task_name}")

    def find_document_in_task(self, file_name):
        '''Метод проверяет наличие/отсутствие прикрепленного к задаче докмуента'''
        xpath = XPathFinder(self.driver)
        target_span_xpath = f'{MyTasksLocators.MY_TASKS_TASKFORM_DOCUMENTS_FILE_TD}[@title="{file_name}"]'
        try:
            xpath.find_visible(target_span_xpath, timeout=3)
            self.logger.info(f"Документ '{file_name}' найден в задаче.")
            return True
        except Exception:
            self.logger.info(f"Документ '{file_name}' не найден в задаче.")
            return False

    def add_required_comment(self, text_comment):
        xpath = XPathFinder(self.driver)
        textarea = xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_REQUIRED_COMMENT_INPUT, timeout=3)
        textarea.click()
        textarea.send_keys(text_comment)
        save_button = xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_REQUIRED_COMMENT_SAVE_BUTTON, timeout=3)
        save_button.click()
        # Ждём уведомления о выполнении действия с задачей
        xpath.find_visible(BaseLocators.POPUP, timeout=5)
        try:
            close_buttons = self.driver.find_elements(By.XPATH, BaseLocators.POPUP_CLOSE)
            if not close_buttons:
                self.logger.info("Нет всплывающих окон для закрытия.")

            for btn in close_buttons:
                try:
                    btn.click()
                except Exception as e:
                    self.logger.warning(f"Не удалось закрыть окно: {e}")

            self.logger.info(f"Закрыто {len(close_buttons)} всплывающих окон.")
        except Exception as e:
            self.logger.error(f"Ошибка при поиске всплывающих окон: {e}")