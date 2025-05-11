import inspect
import datetime
import time
import pyperclip
from selenium.webdriver.common.keys import Keys
'''Импорт класса ActionChains, который позволяет выполнять сложные действия с элементами веб-страницы,
такие как перемещение курсора, двойные клики, перетаскивание объектов и другие действия.'''
from selenium.webdriver.common.action_chains import ActionChains  
'''Импорт исключений, возникающих при работе с Selenium:
TimeoutException – ошибка, возникающая при превышении времени ожидания элемента.
NoSuchElementException – ошибка, возникающая, если элемент не найден на странице.'''
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators.base_locators import BaseLocators # Импорт локаторов, относящихся к базовым элементам страницы
from utils.element_searching import XPathFinder # Импорт вспомогательного класса XPathFinder, который упрощает поиск элементов на странице

class BasePage:
    """Базовый класс, методы которого могут быть использованы на всех (почти) страницах"""

    def __init__(self, driver, logger):
        """Инициализация экземпляра класса.
        :param driver: Экземпляр WebDriver для работы с браузером.
        :param logger: Логгер для ведения журнала событий.
        """
        self.driver = driver
        self.logger = logger
        self.xpath = XPathFinder(driver)  

    def find_click_header_menu(self, button_name, nested_button_name=None):
        """Основной метод обработки кнопок меню Header, включая вложенные элементы.
        :param button_name: Название основной кнопки меню, которую нужно найти и нажать.
        :param nested_button_name: Название вложенного элемента, если требуется его найти и нажать.
        :return: True, если элемент найден и обработан успешно, иначе False.
        """
        
        # Поиск кнопок меню
        btns_headerMenu = self.xpath.find_visible(BaseLocators.HEADER_MENU_BUTTONS, timeout=1, few=True)
        if not btns_headerMenu:
            self.logger.warning("Кнопки Header меню не найдены.")
            return False

        for btn in btns_headerMenu:
            span = self.xpath.find_inside(btn, f'.//span[text()="{button_name}"]', few=True)
            if span and span[0].is_displayed():
                btn.click()
                self.logger.info(f"Кнопка '{button_name}' найдена и кликнута.")

                if nested_button_name:
                    dropdown_elements = self.xpath.find_visible(BaseLocators.HEADER_DROPDOWN_LIST, timeout=1, few=True)
                    nested_items = [
                        item for dropdown in dropdown_elements
                        for item in self.xpath.find_inside(dropdown, f".//div[text()='{nested_button_name}']", few=True)
                    ]
                    if nested_items:
                        nested_items[0].click()
                        self.logger.info(f"Вложенная кнопка '{nested_button_name}' найдена и кликнута.")
                        return True
                    else:
                        self.logger.warning(f"Вложенная кнопка '{nested_button_name}' не найдена.")

                return True  # Если вложенная кнопка не требуется, завершаем обработку

        # Если основная кнопка не найдена, пробуем кликнуть по третьей кнопке ("Ещё")
        if len(btns_headerMenu) >= 3:
            btns_headerMenu[2].click()
            self.logger.info("Клик по кнопке 'Ещё'.")
            dropdown_elements = self.xpath.find_visible(BaseLocators.HEADER_DROPDOWN_LIST, timeout=1, few=True)
        
            for dropdown in dropdown_elements:
                potential_items = self.xpath.find_inside(dropdown, f".//div[text()='{button_name}']", few=True)
                if potential_items:
                    target_item = potential_items[0]

                    if nested_button_name:
                        ActionChains(self.driver).move_to_element(target_item).perform()
                        self.logger.info(f"Наведение на элемент '{button_name}' внутри 'Ещё'.")
                        try:
                            nested_dropdown = self.xpath.find_visible(BaseLocators.HEADER_DROPDOWN_LIST, timeout=1, few=True)
                        except TimeoutException:
                            self.logger.error(f"Dropdown для '{nested_button_name}' не появился вовремя.")
                            return False
                        except NoSuchElementException:
                            self.logger.error(f"Dropdown для '{nested_button_name}' отсутствует в DOM.")
                            return False
                    
                        nested_items = [
                            item for dropdown in nested_dropdown
                            for item in self.xpath.find_inside(dropdown, f".//div[text()='{nested_button_name}']", few=True)
                        ]
                        if nested_items:
                            nested_items[0].click()
                            self.logger.info(f"Вложенный элемент '{nested_button_name}' найден и кликнут.")
                            return True
                        else:
                            self.logger.error(f"Вложенный элемент '{nested_button_name}' не найден.")
                            return False
                    else:
                        target_item.click()
                        self.logger.info(f"Элемент '{button_name}' найден и кликнут.")
                        return True

            self.logger.error(f"Элемент '{button_name}' не найден.")
            return False
        else:
            self.logger.error("Меньше 3 кнопок в меню. Невозможно кликнуть кнопку 'Ещё'.")
            return False

    def find_click_side_menu(self, button_name):
        """Основной метод обработки кнопок бокового меню
        :param button_name: Название кнопки меню
        :return: True, если элемент найден и обработан успешно, иначе False.
        """
        # Поиск кнопок меню
        btns_sideMenu = self.xpath.find_visible(BaseLocators.SIDE_MENU_BUTTONS, timeout=1, few=True)
        if not btns_sideMenu:
            self.logger.error("Кнопки бокового меню не найдены.")
            return False

        for btn in btns_sideMenu:
            span = self.xpath.find_inside(btn, f'.//span[text()="{button_name}"]', few=True)
            if span and span[0].is_displayed():
                btn.click()
                self.logger.info(f"Кнопка '{button_name}' найдена и кликнута.")
                return True
         # Если после цикла кнопка не найдена
        self.logger.error(f"Кнопка '{button_name}' не найдена в боковом меню.")
        return False         
    
    def checking_success_side_menu(self, button_name, title_path, column_path, columns_to_check, scroller_path=None):
        """ Проверяет активность кнопки, соответствие заголовка body, отсутствие всплывающей ошибки и видимость колонок.
        :param button_name: Название кнопки
        :param title_path: XPath заголовка body
        :param column_path: XPath колонок (обязательный)
        :param columns_to_check: Список названий колонок для проверки
        :param scroller_path: XPath скроллера (по умолчанию None)
        """

        xpath = XPathFinder(self.driver)

        # Инициализируем словарь для хранения результатов проверок
        result = {
            "button_active": False,  # Статус активности кнопки
            "body_header_correct": False,  # Соответствие заголовка body кнопке
            "no_popup_error": False,  # Отсутствие всплывающей ошибки
            "columns_visible": False,  # Видимость колонок
            "hidden_columns": []  # Список невидимых колонок
        }

        all_checks_passed = True  # Флаг успешности всех проверок

        # Проверка активности кнопки
        try:
            button = xpath.find_visible(f'{BaseLocators.SIDE_MENU_BUTTONS}/span[text()="{button_name}"]/..', timeout=1)
            result["button_active"] = "active" in button.get_attribute("class") if button else False

            if not result["button_active"]:
                all_checks_passed = False
                self.logger.warning(f"Кнопка '{button_name}' не активна")

        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке активности кнопки '{button_name}'")

        # Проверка заголовка body
        try:
            title_element = xpath.find_visible(f'{title_path}/span', timeout=1)
            title_text = title_element.text.strip() if title_element else ""
            result["body_header_correct"] = title_text == button_name

            if not result["body_header_correct"]:
                all_checks_passed = False
                self.logger.warning(f"Заголовок body ('{title_text}') не соответствует кнопке '{button_name}'")

        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при поиске заголовка body для кнопки '{button_name}'")

        # Проверка отсутствия всплывающей ошибки
        try:
            result["no_popup_error"] = BasePage.check_error(self, False)

            if not result["no_popup_error"]:
                all_checks_passed = False
                self.logger.warning(f"Обнаружена всплывающая ошибка при нажатии {button_name}")

        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке всплывающих ошибок для '{button_name}'")

        # **Добавлена проверка колонок**
        try:
            success, hidden_columns = self.verify_columns_visibility(
                column_path,  # Обязательный XPath колонок
                scroller_path,  # Скроллер (может быть None)
                *columns_to_check  # Передаем список колонок
            )

            result["columns_visible"] = success
            result["hidden_columns"] = hidden_columns

            if not success:
                all_checks_passed = False
                self.logger.warning(f"Некоторые колонки не видны: {hidden_columns}")

        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке колонок в '{button_name}'")

        # Логируем общий результат
        if all_checks_passed:
            self.logger.info(f"Кнопка {button_name} обработана успешно")

        return all_checks_passed, result

    def verify_columns_visibility(self, columns_xpath, scroller_xpath=None, *types):
        """
        Проверяет, видны ли <td> элементы с указанными типами на экране.
        Если элемент выходит за границы, прокручивает скроллер (если есть) или страницу.

        :param columns_xpath: XPath до <td> элементов таблицы
        :param scroller_xpath: XPath до скроллера (если есть), иначе None
        :param types: Список типов для поиска (например, "check", "text")
        :return: (True, []) если все типы видны, иначе (False, список невидимых типов)
        """
        self.logger.info("Начало проверки видимости столбцов таблицы.")
        xpath = XPathFinder(self.driver)

        self.logger.debug("Определение строки со столбцами")
        header_row = self.xpath.find_located(columns_xpath, timeout=5)

        self.logger.debug("Определение всех columns")
        columns = self.xpath.find_inside(header_row, f".//td[contains(@class, 'column')]", few=True)
        hidden_types = set(types)

        scroller = None
        if scroller_xpath:
            self.logger.debug("Загрузка скроллера для горизонтальной прокрутки")
            scroller = self.xpath.find_visible(scroller_xpath, timeout=5)

        for column in columns:
            column_class = column.get_attribute("class")
            column_title = column.get_attribute("title")

            for t in types:
                if t in column_class or t in column_title:
                    self.logger.info(f"Найден столбец '{t}': class='{column_class}', title='{column_title}'.")

                    is_in_viewport = column.is_displayed() and self.driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= window.innerHeight && rect.right <= window.innerWidth);",
                        column
                    )

                    if is_in_viewport:
                        hidden_types.discard(t)
                        self.logger.info(f"Столбец '{t}' видим без прокрутки")
                    else:
                        self.logger.warning(f"Столбец '{t}' не видим на экране. Требуется прокрутка.")

                        if scroller:
                            self.driver.execute_script("arguments[0].scrollLeft = arguments[1].offsetLeft;", scroller, column)
                            self.logger.info(f"Выполнена горизонтальная прокрутка скроллера до столбца '{t}'.")
                        else:
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest'});", column)
                            self.logger.info(f"Выполнена прокрутка страницы до столбца '{t}'.")

                        try:
                            self.logger.debug(f"Ожидание появления столбца '{t}' после прокрутки.")
                            WebDriverWait(self.driver, 3).until(EC.visibility_of(column))
                        except TimeoutException:
                            self.logger.warning(f"Столбец '{t}' не стал видимым после прокрутки.")

                        is_in_viewport = self.driver.execute_script(
                            "var rect = arguments[0].getBoundingClientRect();"
                            "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= window.innerHeight && rect.right <= window.innerWidth);",
                            column
                        )

                        if is_in_viewport:
                            hidden_types.discard(t)
                            self.logger.info(f"Столбец '{t}' теперь видим после прокрутки.")
                        else:
                            self.logger.warning(f"Столбец '{t}' все еще не видим после прокрутки.")

        if hidden_types:
            self.logger.error(f"Не удалось найти или сделать видимыми следующие столбцы: {', '.join(hidden_types)}")
        else:
            self.logger.info("Все указанные столбцы успешно найдены и видимы.")

        return (not hidden_types, list(hidden_types))

    def generate_object_name(self):
        """Генерирует уникальное имя процесса на основе имени функции и временной метки."""
        function_name = inspect.currentframe().f_back.f_code.co_name  # Получаем имя вызывающей функции
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Метка времени
        process_name = f"{function_name}_{timestamp}"  # Формируем имя процесса
        return process_name

    def share_access(self, login_or_group, access_level):
        """Настраивает доступ для пользователя или группы с заданным уровнем."""

        #Проверяем, есть ли уже доступ
        current_setting = None
        try:
            # Ожидаем появления списка пользователей/групп с доступом
            current_setting = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, f'{BaseLocators.SHARE_LIST}/td[contains(@class,"first")]/div/span[@title="{login_or_group}"]/ancestor::tr')))
        except TimeoutException:
            self.logger.info("Проверка доступа не найдена. Устанавливаем новый доступ.")

        # Если доступ уже есть, переходим к настройке уровня доступа
        if current_setting:
            self.logger.info(f"Доступ для '{login_or_group}' уже устанавливался. Переход к настройке уровня доступа.")
        else:
            # Вводим логин или группу
            share_input_xpath = BaseLocators.SHARE_INPUT
            input_element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, share_input_xpath)))
            input_element.send_keys(login_or_group)

            # Ожидаем появления выпадающего списка
            share_dropdown_xpath = BaseLocators.SHARE_DROPDOWN
            dropdown_elements = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, share_dropdown_xpath)))

            # Ищем нужный элемент в выпадающем списке
            for element in dropdown_elements:
                if element.get_attribute("title") == login_or_group:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    element.click()
                    break

            # Ожидаем появления списка пользователей/групп с доступом
            current_setting = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'{BaseLocators.SHARE_LIST}/td[contains(@class,"first")]/div/span[@title="{login_or_group}"]/ancestor::tr'))
            )

        # Кликаем по `td[contains(@class,"int")]`
        access_trigger_xpath = './td[contains(@class,"int")]'
        access_trigger = current_setting.find_element(By.XPATH, access_trigger_xpath)
        access_trigger.click()
        time.sleep(0.5) # Первый клик чтобы сделать строку активной, пауза для стабильности
        access_trigger.click()

        # Кликаем по `SHARE_TRIGGER`
        share_trigger_xpath = BaseLocators.SHARE_TRIGGER
        share_trigger = current_setting.find_element(By.XPATH, share_trigger_xpath)
        share_trigger.click()

        # Выбираем уровень доступа
        share_level_xpath = BaseLocators.SHARE_LEVEL
        level_elements = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, share_level_xpath)))

        for level in level_elements:
            if level.get_attribute("title") == access_level:
                level.click()
                break

        # Сохраняем изменения
        share_save_xpath = BaseLocators.SHARE_SAVE
        save_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, share_save_xpath)))
        save_button.click()

        self.logger.info(f"Доступ для '{login_or_group}' успешно установлен на уровень '{access_level}'.")

    def copy_to(self, new_name):
        """Копирует объект с новым именем.
        :param new_name: Новое имя для копируемого объекта.
        """
        xpath = XPathFinder(self.driver)
        # Ожидаем появления инпута
        input_element = xpath.find_clickable(BaseLocators.COPY_WINDOW_INPUT, timeout=3, few=False)
        input_element.clear()
        input_element.send_keys(new_name)
        # Кликаем по кнопке "Копировать"
        copy_button = xpath.find_clickable(BaseLocators.COPY_WINDOW_COPYBTN, timeout=3, few=False)
        copy_button.click()
        self.logger.info(f"Объект скопирован с именем '{new_name}'.")

    def send_rename(self, current_name, new_name):
        """Переименовывает объект с новым именем.
        :param new_name: Новое имя для переименовываемого объекта.
        """
        xpath = XPathFinder(self.driver)
        rename_path = xpath.find_visible(f'{BaseLocators.BODY_TEXTAREA}/textarea[contains(@title,"{current_name}")]', timeout=3, few=False)
        rename_path.send_keys(f'{new_name}')
        rename_path.send_keys(Keys.ENTER)

    def dialog_window(self, action=True):
        if action:
            # Кнопка "Подтвердить" в диалоговом окне
            confirm_button = self.xpath.find_clickable(
                BaseLocators.DIALOG_WINDOW_CONFIRM, timeout=3, few=False)
            confirm_button.click()
            self.logger.info("Кнопка 'Подтвердить' нажата.")
        else:
            # Кнопка "Отменить" в диалоговом окне
            cancel_button = self.xpath.find_clickable(
                BaseLocators.DIALOG_WINDOW_CANCEL, timeout=3, few=False)
            cancel_button.click()
            self.logger.info("Кнопка 'Отменить' нажата.")

    def check_error(self, should_find_error=True, path=None, has_close_button=True, timeout=1):
            """Проверяет наличие ошибки на странице и, если возможно, закрывает ее.

            :param should_find_error: Ожидается ли наличие ошибки (True) или её отсутствие (False).
            :param path: XPath элемента ошибки, если не указан — используется путь по умолчанию.
            :param has_close_button: Есть ли у ошибки кнопка "Закрыть".
            :param timeout: Время ожидания появления элемента ошибки в DOM.
            :return: True, если ошибка соответствует ожидаемому состоянию; False в противном случае.
            """
            path = path or BaseLocators.ERROR_NOTIFICATION  # Используем базовый путь к ошибке, если не передан кастомный
        
            try:
                # Проверяем, что элемент видим
                self.xpath.find_visible(path, timeout=timeout)

                if should_find_error:
                    self.logger.info(f"Успех: Ошибка найдена: {path}")
                    if has_close_button:
                        try:
                            close_button = self.xpath.find_clickable(BaseLocators.ERROR_CLOSE, timeout=timeout)
                            close_button.click()
                            self.logger.info("Кнопка 'Закрыть' нажата, ошибка скрыта.")
                        except TimeoutException:
                            self.logger.warning("Кнопка 'Закрыть' не кликабельна или отсутствует.")
                    return True
                else:
                    return False
                    #raise Exception(f"Ошибка не должна быть на странице, но найдена: {path}")


            except (TimeoutException, NoSuchElementException):
                if should_find_error:
                    return False
                    #raise Exception(f"Ошибка не найдена, но должна быть — {path}")
                else:
                    self.logger.info(f"Успех: Ошибка отсутствует на странице — {path}")
                    return True

    def click_header_logo_button(self):
        """Ищет и нажимает кнопку HEADER_LOGO_BUTTON. Если кнопка не найдена, выбрасывает TimeoutException."""
        xpath = XPathFinder(self.driver)
        # Ожидание появления и кликабельности кнопки
        logo_button = xpath.find_clickable(BaseLocators.HEADER_LOGO_BUTTON,timeout=3,few=False)
        logo_button.click()
        self.logger.info("Кнопка HEADER_LOGO_BUTTON успешно нажата.")

    def compare_clipboard_with_url(self):
        """Сравнивает скопированную ссылку в буфере обмена с текущим URL браузера."""
    
        # Получаем текущий URL
        current_url = self.driver.current_url
        self.logger.info(f"Текущий URL: {current_url}")

        # Получаем ссылку из буфера обмена
        clipboard_url = pyperclip.paste()
        self.logger.info(f"Ссылка из буфера обмена: {clipboard_url}")

        # Сравниваем ссылки
        if clipboard_url == current_url:
            self.logger.info("Ссылка в буфере обмена совпадает с текущим URL.")
            return True
        else:
            self.logger.warning("Ссылка в буфере обмена НЕ совпадает с текущим URL!")
            return False