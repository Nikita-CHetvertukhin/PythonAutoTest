'''Импорт класса ActionChains, который позволяет выполнять сложные действия с элементами веб-страницы,
такие как перемещение курсора, двойные клики, перетаскивание объектов и другие действия.'''
from selenium.webdriver.common.action_chains import ActionChains  
'''Импорт исключений, возникающих при работе с Selenium:
TimeoutException – ошибка, возникающая при превышении времени ожидания элемента.
NoSuchElementException – ошибка, возникающая, если элемент не найден на странице.'''
from selenium.common.exceptions import TimeoutException, NoSuchElementException  
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
            self.logger.warning("Кнопки меню не найдены.")
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
                        return True

            self.logger.error(f"Элемент '{button_name}' не найден.")
            return False
        else:
            self.logger.error("Меньше 3 кнопок в меню. Невозможно кликнуть кнопку 'Ещё'.")
            return False
    
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