import shutil
import tempfile
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.download_manager import DownloadManager
from settings.variables import URL

class BrowserDriver:
    """Класс для управления веб-драйвером, поддерживающим Chrome и Firefox."""
    def __init__(self, browser_type="chrome"):
        self.browser_type = browser_type.strip().lower()
        self.url = URL
        self.driver = None
        self.temp_profile = None  # Переменная для хранения пути к временной папке

    _chrome_driver_path = None  # Кэшируем ChromeDriver
    _gecko_driver_path = None  # Кэшируем путь к GeckoDriver
    _custom_driver_dir = os.path.join(os.getcwd(), "resources", "drivers")
    _profile_base_dir = os.path.join(os.getcwd(), "resources", "profiles")  # Папка для профилей

    @classmethod
    def ensure_directories(cls):
        """Создаёт необходимые папки, если они не существуют."""
        os.makedirs(cls._custom_driver_dir, exist_ok=True)
        os.makedirs(cls._profile_base_dir, exist_ok=True)

    @classmethod
    def get_latest_chrome_driver(cls):
        """Использует существующий ChromeDriver или скачивает новый."""
        cls.ensure_directories()
        driver_name = "chromedriver.exe" if sys.platform.startswith("win") else "chromedriver"
        chrome_path = os.path.join(cls._custom_driver_dir, driver_name)

        if os.path.exists(chrome_path):
            return chrome_path

        # Скачиваем драйвер
        downloaded_path = ChromeDriverManager().install()

        # Копируем в кастомную папку
        shutil.copy(downloaded_path, chrome_path)

        return chrome_path

    @classmethod
    def get_latest_gecko_driver(cls):
        """Ищет GeckoDriver в `resources/drivers` или загружает новый."""
        cls.ensure_directories()
        driver_name = "geckodriver.exe" if sys.platform.startswith("win") else "geckodriver"
        gecko_path = os.path.join(cls._custom_driver_dir, driver_name)

        if os.path.exists(gecko_path):
            return gecko_path

        # Если драйвера нет — скачиваем новый и сохраняем в `drivers`
        downloaded_path = GeckoDriverManager().install()
        shutil.copy(downloaded_path, gecko_path)

        return gecko_path

    @classmethod
    def get_latest_edge_driver(cls):
        """Ищет Edge WebDriver в `resources/drivers` или загружает новый."""
        cls.ensure_directories()
        driver_name = "msedgedriver.exe" if sys.platform.startswith("win") else "msedgedriver"
        edge_path = os.path.join(cls._custom_driver_dir, driver_name)

        if os.path.exists(edge_path):
            return edge_path

        # Скачиваем драйвер и копируем в кастомную папку
        downloaded_path = EdgeChromiumDriverManager().install()
        shutil.copy(downloaded_path, edge_path)

        return edge_path

    def create_temp_profile(self):
        """Создаёт временную папку профиля в 'resources/profiles'."""
        self.temp_profile = tempfile.mkdtemp(dir=self._profile_base_dir, prefix=f"{self.browser_type}-profile-{os.getpid()}-")

    def initialize_driver(self):
        """Инициализация WebDriver с временным профилем и настройками."""
        self.ensure_directories()
        self.create_temp_profile()  # Создаём профиль

        if self.browser_type == "chrome":
            download_manager = DownloadManager()
            download_dir = download_manager.get_download_path()
            service = Service(self.get_latest_chrome_driver())

            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {
                "download.default_directory": download_dir,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "download.prompt_for_download": False,
                "profile.default_content_setting_values.notifications": 2
            })
            # Важно для Docker
            options.add_argument("--no-sandbox")
            # Блокировка всплывающих окон и уведомлений
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
            # Размер окна
            options.add_argument("--window-size=1920,1080")
            # Оптимизация памяти и производительности
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            # Отключение защиты загрузок
            options.add_argument("--safebrowsing-disable-download-protection")
            options.add_argument("--disable-blink-features=DownloadUI")
            # Отключение GPU и рендеринга
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-webgl")
            options.add_argument("--disable-gpu-compositing")
            options.add_argument("--disable-angle")
            options.add_argument("--disable-accelerated-2d-canvas")
            options.add_argument("--disable-accelerated-video-decode")
            # Только fatal (без предупреждений из-за GPU и тд)
            options.add_argument("--log-level=3")
            # Для контейнера (без UI)
            options.add_argument("--headless=new")
            
            # Добавляем временный профиль
            options.add_argument(f"--user-data-dir={self.temp_profile}")

            self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser_type == "firefox":
            download_manager = DownloadManager()
            download_dir = download_manager.get_download_path()
            # Используем кэшированный драйвер
            gecko_path = self.get_latest_gecko_driver()
            if not gecko_path:
                raise RuntimeError("GeckoDriver не найден или не установлен.")
            service = FirefoxService(executable_path=gecko_path)

            options = webdriver.FirefoxOptions()
            options.set_preference("browser.download.dir", download_dir)
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            options.set_preference("browser.download.useDownloadDir", True)
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("permissions.default.desktop-notification", 2)
            options.set_preference("pdfjs.disabled", True)  # Отключает встроенный PDF viewer
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            # Для контейнера (без UI)
            options.add_argument("--headless")

            # Добавляем временный профиль
            options.set_preference("browser.profile.path", self.temp_profile)

            self.driver = webdriver.Firefox(service=service, options=options)

        elif self.browser_type == "edge":
            download_manager = DownloadManager()
            download_dir = download_manager.get_download_path()
            service = EdgeService(self.get_latest_edge_driver())

            options = webdriver.EdgeOptions()
            options.add_experimental_option("prefs", {
                "download.default_directory": download_dir,  # Указываем папку загрузок
                "download.prompt_for_download": False,  # Отключает запрос перед скачиванием
                "safebrowsing.enabled": True,  # Включает безопасные загрузки
            })
            options.add_argument("--no-sandbox")  # Отключает песочницу, важно для Docker
            options.add_argument("--disable-dev-shm-usage") # КРИТИЧЕСКИ ВАЖНО ДЛЯ EDGE В КОНТЕЙНЕРЕ
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-first-run")  # Отключает окно первого запуска
            options.add_argument("--no-default-browser-check")  # Запрещает проверку браузера по умолчанию
            options.add_argument("--disable-features=msEdgeWelcomePage,PreloadMediaEngagementData,PreloadNetworkData")
            # Для контейнера (без UI)
            options.add_argument("--headless=new")

            # Указываем путь временного профиля
            options.add_argument(f"--user-data-dir={self.temp_profile}")
        
            self.driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError(f"Браузер '{self.browser_type}' не поддерживается.")
        
        self.driver.get(self.url)
        return self.driver

    def cleanup(self):
        """Закрывает драйвер и удаляет временный профиль."""
        if self.driver:
            self.driver.quit()
        if self.temp_profile:
            shutil.rmtree(self.temp_profile, ignore_errors=True)  # Удаляем временную папку