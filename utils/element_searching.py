from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from utils.active_driver_tracker import set_active_driver

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
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"find_located: элемент не появился в DOM за {wait_time}с. XPath: {path}"
            ) from e
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_visible(self, path, timeout=None, few=None, scroll=False):
        """Проверяет, что элемент(ы) видим."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"find_visible: элемент не стал видимым за {wait_time}с. XPath: {path}"
            ) from e
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_clickable(self, path, timeout=None, few=None, scroll=False):
        """Проверяет, что элемент(ы) кликабелен."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few
        # Ищем и скроллим до элемента
        if scroll:
            element = self.driver.find_element(By.XPATH, path)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        # Проверяем кликабельность
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, path))
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"find_clickable: элемент не стал кликабельным за {wait_time}с. XPath: {path}"
            ) from e
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def find_invisible(self, path, timeout=None, few=None):
        """Проверяет, что элемент(ы) не видим."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout
        search_mode = few if few is not None else self.few

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located((By.XPATH, path))
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"find_invisible: элемент не исчез/не стал невидимым за {wait_time}с. XPath: {path}"
            ) from e
        return self.driver.find_elements(By.XPATH, path) if search_mode else self.driver.find_element(By.XPATH, path)

    def wait_visible(self, element, timeout=None):
        """Ждёт, пока уже найденный WebElement станет видимым."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout

        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of(element))
        except TimeoutException as e:
            raise TimeoutException(
                f"wait_visible: элемент не стал видимым за {wait_time}с."
            ) from e
        return element

    def wait_clickable(self, element, timeout=None):
        """Ждёт, пока уже найденный WebElement станет кликабельным."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout

        try:
            WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(element))
        except TimeoutException as e:
            raise TimeoutException(
                f"wait_clickable: элемент не стал кликабельным за {wait_time}с."
            ) from e
        return element

    def wait_invisible(self, element, timeout=None):
        """Ждёт, пока уже найденный WebElement станет невидимым/исчезнет."""
        set_active_driver(self.driver)
        wait_time = timeout if timeout is not None else self.timeout

        try:
            WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element(element))
        except TimeoutException as e:
            raise TimeoutException(
                f"wait_invisible: элемент не исчез/не стал невидимым за {wait_time}с."
            ) from e
        return element

    def not_find(self, path: str, timeout: int = None, few: bool = None):
        """Проверяет, что элемент(ы) отсутствуют в DOM по заданному XPath."""
        set_active_driver(self.driver)
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
        set_active_driver(self.driver)
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
        set_active_driver(self.driver)
        search_mode = few if few is not None else self.few
        return element.find_elements(By.XPATH, path) if search_mode else element.find_element(By.XPATH, path)