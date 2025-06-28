from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class XPathFinder:
    """Утилиты для поиска элементов по XPath с использованием Selenium."""

    def __init__(self, driver, timeout=10, few=False):
        """Инициализация класса.
        :param driver: WebDriver для взаимодействия с браузером.
        :param timeout: Время ожидания элемента (по умолчанию 10 секунд).
        :param few: Если True, методы ищут список элементов, иначе один.
        """
        self.driver = driver
        self.timeout = timeout
        self.few = few  # Контролирует режим поиска элементов (один или список)

    def find_located(self, path, timeout=None, few=None):
        """Проверяет, что элемент(ы) присутствует в DOM."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_visible(self, path, timeout=None, few=None, scroll=False):
        """Проверяет, что элемент(ы) видим."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        element = WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_clickable(self, path, timeout=None, few=None, scroll=False):
        """Проверяет, что элемент(ы) кликабелен."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, path))
        )
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_invisible(self, path, timeout=None, few=None):
        """Проверяет, что элемент(ы) не видим."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        WebDriverWait(self.driver, wait_time).until(
            EC.invisibility_of_element_located((By.XPATH, path))
        )
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def not_find(self, path: str, timeout: int = None, few: bool = None):
        """Проверяет, что элемент(ы) отсутствуют в DOM по заданному XPath."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        try:
            if search_mode:
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, path))
                )
            else:
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, path))
                )
            # Нашёл элемент
            return False
        except TimeoutException:
            # Не нашёл в течение таймаута → считаем, что отсутствуют
            return True

    def wait_until_elements_not_present(self, path: str, timeout: int = None, few: bool = None):
        """Ждёт, пока элемент(ы) исчезнут из DOM."""
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        try:
            WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_all_elements_located((By.XPATH, path)) if search_mode
                else EC.presence_of_element_located((By.XPATH, path))
            )
            return True
        except TimeoutException:
            return False

    def find_inside(self, element, path, few=None):
        """Ищет элементы внутри другого элемента (WebElement).
        :param element: Родительский элемент (`WebElement`).
        :param path: XPath вложенного элемента.
        :param few: Если True, ищет список элементов, иначе один (по умолчанию используется `self.few`).
        :return: Один или список `WebElement`, найденных внутри `element`.
        """
        search_mode = few if few is not None else self.few
        return element.find_elements(By.XPATH, path) if search_mode else element.find_element(By.XPATH, path)