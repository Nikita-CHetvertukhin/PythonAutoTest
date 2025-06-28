import time
from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.my_tasks_locators import MyTasksLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
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
        input_element.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_element.send_keys(Keys.DELETE)  # Удалить выделенное
        input_element.send_keys(process_name)
        self.logger.info(f"Имя процесса '{process_name}' введено в поле типа задачи")
        if xpath.find_clickable(f'{MyTasksLocators.MY_TASKS_TASK_TYPE_TRS}[contains(@title,"{process_name}")]', timeout=5):
            self.logger.info(f"Процесс '{process_name}' найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return True
        else:
            self.logger.error(f"Процесс '{process_name}' не найден в списке типов задач")
            xpath.find_clickable(MyTasksLocators.MY_TASKS_CANCEL_BUTTON, timeout=3).click()
            self.logger.info("Окно создания задачи закрыто")
            return False

    def create_task(self, task_name, task_description=None, task_type=None, deadline=None, executor=None):

        self.xpath.find_clickable(MyTasksLocators.MY_TASKS_CREATE_TASK_BUTTON, timeout=3).click()
        
        input_name = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_NAME_INPUT, timeout=3)
        input_name.click()  # Кликаем по полю ввода названия задачи
        input_name.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        input_name.send_keys(Keys.DELETE)  # Удалить
        input_name.send_keys(task_name)
        self.logger.info("Название задачи успешно установлено.")

        if task_description:
            input_description = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_DESCRIPTION_INPUT, timeout=3)
            input_description.click()  # Кликаем по полю ввода описания задачи
            input_description.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_description.send_keys(Keys.DELETE)  # Удалить
            input_description.send_keys(task_description)
            self.logger.info("Описание задачи успешно установлено.")

        if task_type:
            input_type = self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASK_TYPE_INPUT, timeout=5)
            input_type.click()  # Кликаем по полю ввода типа задачи
            input_type.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
            input_type.send_keys(Keys.DELETE)  # Удалить выделенное
            input_type.send_keys(task_type)
            self.logger.info(f"Имя процесса '{task_type}' введено в поле типа задачи")
            succes_path = f'{MyTasksLocators.MY_TASKS_TASK_TYPE_TRS}[contains(@title,"{task_type}")]'
            if self.xpath.find_clickable(succes_path, timeout=3):
                self.logger.info(f"Процесс '{task_type}' найден в списке типов задач")
                self.xpath.find_clickable(succes_path, timeout=3).click()
            else:
                self.logger.error(f"Процесс '{task_type}' не найден в списке типов задач")

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
        self.xpath.find_clickable(MyTasksLocators.MY_TASKS_TASKFORM_CLOSE_BUTTON, timeout=3).click()
        self.logger.info("Подзадача успешно создана.")

    def find_task_by_name(self, name):
        """Ищет процесс по имени и скроллит до него, если он не виден."""
        xpath = XPathFinder(self.driver)

        try:
            # Формируем xpath до интересуещего процесса
            target_xpath = f'{MyTasksLocators.MY_TASKS_LIST}/span[@title="{name}"]'

            # Ищем сам элемент внутри списка
            process_element = xpath.find_located(target_xpath, timeout=3, few=False)

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
        select_xpath = MyTasksLocators.MY_TASKS_TASKFORM_EXECUTOR_TRS.format(executor_login=executor_login)
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
                time.sleep(1)  # Дать списку время появиться
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
        '''Метод проверяет успешное скачивания истории таска у указанном формате'''
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