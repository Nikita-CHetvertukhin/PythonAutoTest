import inspect
from settings.variables import ADMIN_LOGIN, ADMIN_PASSWORD_MD5
import datetime
import time
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
# API для загрузки файла
from api.auth_client import AuthClient
from api.upload_client import FileUploadClient
from api.rename_client import RenameClient

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

    def exit_from_account(self):
        """Метод для выхода из УЗ."""
        try:
            self.logger.info("Поиск и клик иконки УЗ в хедере")
            account_button = self.xpath.find_clickable(BaseLocators.HEADER_ACCOUNT_BUTTON, timeout=3, few=False)
            account_button.click()
            self.logger.info("Кнопка личного кабинета нажата. Переход к поиску и клику кнопки выхода.")
            signout_button = self.xpath.find_clickable(BaseLocators.ACCOUNT_SIGNOUT, timeout=3, few=False)
            signout_button.click()
            self.logger.info("Кнопка 'Выйти' нажата. Выход из учетной записи выполнен.")
        except Exception as e:
            self.logger.error(f"Не удалось выйти из учетной записи: {str(e)}")
            raise

    def find_click_header_menu(self, button_name, nested_button_name=None):
        """Основной метод обработки кнопок меню Header, включая вложенные элементы.
        :param button_name: Название основной кнопки меню, которую нужно найти и нажать.
        :param nested_button_name: Название вложенного элемента, если требуется его найти и нажать.
        :return: True, если элемент найден и обработан успешно, иначе False.
        """
        
        # Поиск кнопок меню
        try:
            btns_headerMenu = self.xpath.find_visible(BaseLocators.HEADER_MENU_BUTTONS, timeout=5, few=True)
        except TimeoutException:
            btns_headerMenu = []
        if not btns_headerMenu:
            self.logger.warning("Кнопки Header меню не найдены. Пробуем через Doczilla Pro.")
        else:
            for btn in btns_headerMenu:
                label = self.xpath.find_inside(btn, f'.//label[text()="{button_name}"]/parent::button', few=True)
                if label and label[0].is_displayed():
                    btn.click()
                    self.logger.info(f"Кнопка '{button_name}' найдена и кликнута.")

                    if nested_button_name:
                        dropdown_elements = self.xpath.find_visible(BaseLocators.HEADER_DROPDOWN_LIST, timeout=1, few=True)
                        nested_items = [
                            item for dropdown in dropdown_elements
                            for item in self.xpath.find_inside(dropdown, f".//label[text()='{nested_button_name}']/parent::div", few=True)
                        ]
                        if nested_items:
                            nested_items[0].click()
                            self.logger.info(f"Вложенная кнопка '{nested_button_name}' найдена и кликнута.")
                            return True
                        else:
                            self.logger.warning(f"Вложенная кнопка '{nested_button_name}' не найдена.")

                    return True  # Если вложенная кнопка не требуется, завершаем обработку

        # Если основная кнопка не найдена, пробуем кликнуть по кнопке Doczilla Pro в лого
        doczilla_pro = self.xpath.find_clickable(BaseLocators.HEADER_DOCZILLA_BUTTON, timeout=1)
        doczilla_pro.click()
        self.logger.info("Клик по кнопке 'Doczilla Pro'")
        dropdown_elements = self.xpath.find_visible(BaseLocators.HEADER_DROPDOWN_LIST, timeout=1, few=True)
        
        for dropdown in dropdown_elements:
            potential_items = self.xpath.find_inside(dropdown, f"./div/label[text()='{button_name}']/parent::div", few=True)
            if potential_items:
                target_item = potential_items[0]

                if nested_button_name:
                    ActionChains(self.driver).move_to_element(target_item).perform()
                    self.logger.info(f"Наведение на элемент '{button_name}' внутри 'Doczilla Pro'.")
                    try:
                        nested_dropdown = self.xpath.find_inside(dropdown, BaseLocators.HEADER_DROPDOWN_LIST, few=True)
                    except TimeoutException:
                        self.logger.error(f"Dropdown для '{nested_button_name}' не появился вовремя.")
                        return False
                    except NoSuchElementException:
                        self.logger.error(f"Dropdown для '{nested_button_name}' отсутствует в DOM.")
                        return False
                    
                    nested_items = [
                        item for dropdown in nested_dropdown
                        for item in self.xpath.find_inside(dropdown, f".//label[text()='{nested_button_name}']/parent::div", few=True)
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
                try:
                    # 1 Попытка найти строки сразу
                    try:
                        WebDriverWait(self.driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, BaseLocators.BODY_LIST))
                        )
                        self.logger.info("Строки таблицы найдены сразу.")
                        return True
                    except TimeoutException:
                        self.logger.info("Строки сразу не найдены.")

                     # 2️ Проверка наличия индикатора загрузки
                    try:
                        loading_icon = WebDriverWait(self.driver, 1).until(
                            EC.visibility_of_element_located((By.XPATH, BaseLocators.BODY_STATUS))
                        )
                        self.logger.info("Обнаружен индикатор загрузки. Ожидание завершения...")
                        try:
                            WebDriverWait(self.driver, 5).until(
                                EC.invisibility_of_element(loading_icon)
                            )
                            self.logger.info("Индикатор загрузки исчез. Повторная проверка строк...")
                            try:
                                WebDriverWait(self.driver, 1).until(
                                    EC.presence_of_element_located((By.XPATH, BaseLocators.BODY_LIST))
                                )
                                self.logger.info("Строки таблицы загружены после ожидания.")
                                return True
                            except TimeoutException:
                                self.logger.info("Страница пуста после исчезновения индикатора.")
                        except TimeoutException:
                            self.logger.warning("Страница не загружена в течение 5 секунд.")
                            return False
                    except TimeoutException:
                        self.logger.info("Индикатор загрузки не найден. Повторная проверка строк...")
                        try:
                            WebDriverWait(self.driver, 1).until(
                                EC.presence_of_element_located((By.XPATH, BaseLocators.BODY_LIST))
                            )
                            self.logger.info("Строки таблицы найдены.")
                            return True
                        except TimeoutException:
                            self.logger.warning("Страница пуста. Строки таблицы не найдены.")
                            return True
                except Exception as e:
                    self.logger.error(f"Ошибка при ожидании загрузки таблицы в течение 5 секунд: {e}")
                    return False

         # Если после цикла кнопка не найдена
        self.logger.error(f"Кнопка '{button_name}' не найдена в боковом меню.")
        return False         
    
    def find_file_by_name(self, name, format_file=None):
        """Ищет файл по имени и скроллит до него, если он не виден.
        Аргумент format позволяет указать формат файла, если необходимо.
        Возможные значения fromats: 'docz', 'docx', 'dotx', 'folder'.
        """
        xpath = XPathFinder(self.driver)
        # Проверяем допустимые форматы файлов если указаны
        VALID_FORMATS = {"docz", "docx", 'dotx', "folder"}
        if format_file and format_file not in VALID_FORMATS:
            self.logger.warning(f"Недопустимый формат файла: '{format_file}'. Допустимые: {VALID_FORMATS}")
            return None

        try:
            # Формируем xpath до интересуещего процесса
            target_xpath = f'{BaseLocators.BODY_NAMES}/span[@title="{name}"]'

            # Ищем сам элемент внутри списка
            file_element = xpath.find_located(target_xpath, timeout=1, few=False)

            if file_element:
                self.logger.info(f"Файл '{name}' найден в DOM.")

                xpath.find_visible(target_xpath, timeout=5, few=False)
                xpath.find_clickable(target_xpath, timeout=5, few=False)

                self.logger.info(f"Файл '{name}' отображается на экране и доступен")
                # Проверяем формат если указан
                if format_file:
                    icon_xpath = f'{target_xpath}/preceding-sibling::i[contains(@class,"{format_file}")]'
                    try:
                        xpath.find_visible(icon_xpath, timeout=3)
                        self.logger.info(f"Файл '{name}' подтвержден формат '{format_file}'.")
                    except TimeoutException:
                        message = f"Файл '{name}' найден, но формат '{format_file}' не подтверждён."
                        self.logger.error(f"Файл '{name}' найден, но формат '{format_file}' не подтверждён.")
                        raise AssertionError(message)

                return file_element

        except TimeoutException:
            self.logger.warning(f"Файл '{name}' не найден в DOM!")
            return None

    def checking_success_side_menu(self, button_name, title_path, column_path, columns_to_check):
        """Проверяет активность кнопки, соответствие заголовка body, отсутствие ошибки и видимость колонок."""
        xpath = XPathFinder(self.driver)

        result = {
            "button_active": False,
            "body_header_correct": False,
            "no_popup_error": False,
            "columns_visible": False,
            "hidden_columns": []
        }

        all_checks_passed = True

        try:
            button = xpath.find_visible(f'{BaseLocators.SIDE_MENU_BUTTONS}/span[text()="{button_name}"]/..', timeout=1)
            result["button_active"] = "active" in button.get_attribute("class") if button else False
            if not result["button_active"]:
                all_checks_passed = False
                self.logger.warning(f"Кнопка '{button_name}' не активна")
        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке активности кнопки '{button_name}'")

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

        try:
            result["no_popup_error"] = BasePage.check_error(self, False)
            if not result["no_popup_error"]:
                all_checks_passed = False
                self.logger.warning(f"Обнаружена всплывающая ошибка при нажатии {button_name}")
        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке всплывающих ошибок для '{button_name}'")

        try:
            success, hidden_columns = self.verify_columns_visibility(column_path, *columns_to_check)
            result["columns_visible"] = success
            result["hidden_columns"] = hidden_columns
            if not success:
                all_checks_passed = False
                self.logger.warning(f"Некоторые колонки не видны: {hidden_columns}")
        except Exception:
            all_checks_passed = False
            self.logger.exception(f"Ошибка при проверке колонок в '{button_name}'")

        if all_checks_passed:
            self.logger.info(f"Кнопка {button_name} обработана успешно")

        return all_checks_passed, result

    def verify_columns_visibility(self, columns_xpath, *types):
        """Проверяет, что <td> элементы с указанными типами видимы на странице."""
        self.logger.info("Начало проверки видимости столбцов таблицы.")
        self.xpath = XPathFinder(self.driver)

        header_row = self.xpath.find_located(columns_xpath, timeout=5)
        columns = self.xpath.find_inside(header_row, ".//td[contains(@class, 'column')]", few=True)
        hidden_types = set(types)

        for column in columns:
            column_class = column.get_attribute("class")
            column_title = column.get_attribute("title")

            for t in types:
                if t in column_class or t in column_title:
                    self.logger.info(f"Найден столбец '{t}': class='{column_class}', title='{column_title}'.")

                    try:
                        # Убедимся, что элемент действительно видим
                        WebDriverWait(self.driver, 1).until(EC.visibility_of(column))
                        hidden_types.discard(t)
                        self.logger.info(f"Столбец '{t}' успешно найден и видим.")
                    except TimeoutException:
                        self.logger.warning(f"Столбец '{t}' не найден как видимый.")

        if hidden_types:
            self.logger.error(f"Невидимые или отсутствующие столбцы: {', '.join(hidden_types)}")
        else:
            self.logger.info("Все указанные столбцы успешно найдены и видимы.")

        return not hidden_types, list(hidden_types)

    def generate_object_name(self):
        """Генерирует уникальное имя процесса на основе имени функции и временной метки."""
        function_name = inspect.currentframe().f_back.f_code.co_name  # Получаем имя вызывающей функции
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Метка времени
        process_name = f"{function_name}_{timestamp}"  # Формируем имя процесса
        return process_name

    def share_access(self, login_or_group=None, access_level=None, action="set", logins_and_access=None):
        """
        Настраивает или проверяет доступ для пользователя/группы.

        :param login_or_group: Логин или группа (используется при action='set')
        :param access_level: Уровень доступа (используется при action='set')
        :param action: 'set' — установить доступ, 'check' — проверить соответствие
        :param logins_and_access: Список пар (логин, уровень доступа) для проверки (используется при action='check')
        """
        xpath = XPathFinder(self.driver)

        if action == "check":
            mismatches = []

            for login, expected_level in logins_and_access:
                try:
                    row_xpath = f'{BaseLocators.SHARE_LIST}/td[contains(@class,"first")]/div/span[@title="{login}"]/ancestor::tr'
                    row_element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, row_xpath))
                    )
                    access_cell = row_element.find_element(By.XPATH, './td[contains(@class,"int")]')
                    actual_level = access_cell.text.strip()

                    if actual_level != expected_level:
                        mismatches.append((login, actual_level, expected_level))
                        self.logger.warning(f"Несоответствие: '{login}' — текущий уровень '{actual_level}', ожидаемый '{expected_level}'")
                    else:
                        self.logger.info(f"Проверка пройдена: '{login}' имеет уровень доступа '{actual_level}'")

                except TimeoutException:
                    mismatches.append((login, None, expected_level))
                    self.logger.warning(f"Пользователь '{login}' не найден в списке доступа")

            # Закрываем окно доступа
            xpath.find_clickable(BaseLocators.SHARE_CANCEL, timeout=3).click()
            if mismatches:
                self.logger.error(f"Обнаружены несоответствия: {mismatches}")
                return False, mismatches
            else:
                self.logger.info("Все уровни доступа соответствуют ожидаемым")
                return True

        # Если установка доступа
        current_setting = None
        try:
            current_setting = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, f'{BaseLocators.SHARE_LIST}/td[contains(@class,"first")]/div/span[@title="{login_or_group}"]/ancestor::tr'))
            )
        except TimeoutException:
            self.logger.info("Проверка доступа не найдена. Устанавливаем новый доступ.")

        if not current_setting:
            input_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, BaseLocators.SHARE_INPUT))
            )
            input_element.send_keys(login_or_group)

            dropdown_elements = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, BaseLocators.SHARE_DROPDOWN))
            )

            for element in dropdown_elements:
                if element.get_attribute("title") == login_or_group:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    element.click()
                    break

            current_setting = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'{BaseLocators.SHARE_LIST}/td[contains(@class,"first")]/div/span[@title="{login_or_group}"]/ancestor::tr'))
            )

        access_trigger = current_setting.find_element(By.XPATH, './td[contains(@class,"int")]')
        access_trigger.click()
        time.sleep(0.5)
        access_trigger.click()

        share_trigger = current_setting.find_element(By.XPATH, BaseLocators.SHARE_TRIGGER)
        share_trigger.click()

        level_elements = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, BaseLocators.SHARE_LEVEL))
        )

        for level in level_elements:
            if level.get_attribute("title") == access_level:
                level.click()
                break

        save_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, BaseLocators.SHARE_SAVE))
        )
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

    def publish_to(self, logins_groups, directory=None):
        '''Публикует объект из окна публикации на Логин/логины УЗ/групп, если указана директория выбирает дополнительно директорию'''
        time.sleep(1)
        if directory:
            input_directory_element = self.xpath.find_clickable(BaseLocators.PUBLISH_DIRECTORY_INPUT, timeout=3, few=False)
            input_directory_element.send_keys(directory)
            self.xpath.find_clickable(f'{BaseLocators.PUBLISH_DIRECTORY_DROPDOWN}[contains(@title,"{directory}")]').click()
            self.logger.info(f"Каталог публикации '{directory}' установлен")
        # logins_groups получаем массив, который может состоять из одного или несколкьих элементов
        for login in logins_groups:
            input_logins_element = self.xpath.find_clickable(BaseLocators.PUBLISH_INPUT, timeout=3, few=False)
            input_logins_element.send_keys(login)
            self.logger.info(f"Попытка поиска {login}")
            self.xpath.find_clickable(f'{BaseLocators.PUBLISH_DROPDOWN}[contains(@title,"{login}")]').click()
            # Проверка, что появилась запись на публикацию
            try:
                self.xpath.find_visible(f'{BaseLocators.PUBLISH_LIST}//span[contains(@title,"{login}")]')
            except Exception as e:
                self.logger.error(f"Ошибка при добавлении логина/группы '{login}': {e}")
                raise RuntimeError(f"Публикация прервана: логин/группа '{login}' не появился(а) в списке") from e
        self.xpath.find_clickable(BaseLocators.PUBLISH_FINISH, timeout=3).click()
        self.logger.info("Публикация завершена")

    def move_to(self, folder_name=None, section_name=None, new_name=None):
        """Метод перемещает выбранный файл (уже из окна перемещения) в выбранную секцию/папку с новым названием (опицонально)"""
        target_folder_xpath = f'{BaseLocators.COPY_WINDOW_LIST}/td[contains(@class,"first")]//span[contains(@title,"{folder_name}")]'
        # Если задана секция ("Мои файлы" по умолчанию)
        if section_name:
            """Дописать"""
        # Если задано новое имя (опционально)
        if new_name:
            input_element = self.xpath.find_clickable(BaseLocators.COPY_WINDOW_INPUT, timeout=3, few=False)
            input_element.clear()
            input_element.send_keys(new_name)
            self.logger.info(f'При перемещении задано новое имя {new_name}')
        # Если перемещаем в определенную папку (тоже опционально, т.к. можем просто переместить из общих дисков в корень "Мои файлы", например)
        if folder_name:
            self.xpath.find_clickable(target_folder_xpath, timeout=3).click()
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)  # Пауза для стабильности
            self.logger.info(f'Двойной клик по каталогу {folder_name}')

        # Кликаем по кнопке "Переместить"
        moved_button = self.xpath.find_clickable(BaseLocators.COPY_WINDOW_COPYBTN, timeout=3, few=False)
        moved_button.click()
        self.logger.info(f"Объект перемещен в секцию {section_name} в папку {folder_name}.")

    def send_rename(self, current_name, new_name):
        """Переименовывает объект с новым именем.
        :param new_name: Новое имя для переименовываемого объекта.
        """
        xpath = XPathFinder(self.driver)
        self.logger.info(f"Переименование: current='{current_name}', new='{new_name}'")
        rename_path = xpath.find_visible(f'{BaseLocators.BODY_TEXTAREA}', timeout=3, few=False)
        self.logger.info(f"Xpath {rename_path} найден")
        rename_path.send_keys(f'{new_name}')
        self.logger.info(f"Имя объекта '{current_name}' изменено на '{new_name}'")
        next_td_path = xpath.find_visible(f'{BaseLocators.BODY_TEXTAREA}/ancestor::td[1]/following-sibling::td[contains(@field,"1")]', timeout=3, few=False)
        self.logger.info(f"Xpath {next_td_path} найден")
        next_td_path.click()  # Кликаем по следующему td, чтобы сохранить изменения

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
        logo_button = xpath.find_clickable(BaseLocators.HEADER_LOGO_BUTTON,timeout=10,few=False)
        logo_button.click()
        self.logger.info("Кнопка HEADER_LOGO_BUTTON успешно нажата.")

    def close_all_windows(self):
        """Метод ищет все всплывающие окна и закрывает их, если найдены."""
        xpath = XPathFinder(self.driver)
        xpath.find_visible(BaseLocators.POPUP, timeout=5)
        try:
            close_buttons = self.driver.find_elements(By.XPATH, BaseLocators.POPUP_CLOSE)
            if not close_buttons:
                self.logger.info("Нет всплывающих окон для закрытия.")
                return False

            for btn in close_buttons:
                try:
                    btn.click()
                except Exception as e:
                    self.logger.warning(f"Не удалось закрыть окно: {e}")

            # Ждём, пока попапы исчезнут из DOM
            WebDriverWait(self.driver, 5).until(
                lambda d: not d.find_elements(By.XPATH, BaseLocators.POPUP)
            )
            self.logger.info(f"Закрыто {len(close_buttons)} всплывающих окон.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при поиске всплывающих окон: {e}")
            return False

    def upload_file(self, upload_file_name, new_name):
        # Создание через API: Загрузка и переименование
        auth_client = AuthClient(login={ADMIN_LOGIN}, password={ADMIN_PASSWORD_MD5})
        session_id = auth_client.get_session()

        upload_client = FileUploadClient(session_id=session_id)
        record_id = upload_client.upload_file(upload_file_name)

        rename_client = RenameClient(session_id=session_id)
        file_name = rename_client.rename_by_recordid(record_id, new_name)
        return file_name

    def popup_action(self, action=True):
        """Метод для обработки действий в всплывающем окне."""
        xpath = XPathFinder(self.driver)
        if action:
            # Кнопка подтверждения действия в всплывающем окне
            confirm_button = xpath.find_clickable(BaseLocators.POPUP_CONFIRM, timeout=3, few=False)
            confirm_button.click()
            self.logger.info("Кнопка подтверждения действия в всплывающем окне нажата.")
        else:
            # Кнопка отмены действия в всплывающем окне
            cancel_button = xpath.find_clickable(BaseLocators.POPUP_CANCEL, timeout=3, few=False)
            cancel_button.click()
            self.logger.info(
                "Кнопка отмены действия в всплывающем окне нажата.")