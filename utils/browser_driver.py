import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.download_manager import DownloadManager
from settings.variables import URL

class BrowserDriver:
    """Класс для управления веб-драйвером, поддерживающим Chrome и Firefox."""
    def __init__(self, browser_type="chrome"):
        self.browser_type = browser_type.lower()
        self.url = URL
        self.driver = None
        self.temp_profile = None  # Переменная для хранения пути к временной папке

    def initialize_driver(self):
        """Инициализация WebDriver в зависимости от указанного типа браузера."""
        if self.browser_type == "chrome":
            download_manager = DownloadManager()
            download_dir = download_manager.get_download_path()
            service = Service(ChromeDriverManager().install())

            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {
                "download.default_directory": download_dir,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "download.prompt_for_download": False,
                "profile.default_content_setting_values.notifications": 2  # Отключает уведомления
            })
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-software-rasterizer")  # Отключает рендеринг через CPU
            options.add_argument("--disable-extensions")  # Отключает расширения, которые могут влиять на загрузки
            options.add_argument("--safebrowsing-disable-download-protection")  # Отключает защиту загрузок
            options.add_argument("--disable-popup-blocking")  # Отключает всплывающие окна
            options.add_argument("--disable-blink-features=DownloadUI")  # Отключает UI загрузок

            # Создаём временную папку для профиля Chrome
            self.temp_profile = tempfile.mkdtemp(prefix='chrome-profile-')
            options.add_argument(f"--user-data-dir={self.temp_profile}")

            self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser_type == "firefox":
            service = FirefoxService(GeckoDriverManager().install())

            options = webdriver.FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("dom.disable_open_during_load", True)
            options.set_preference("permissions.default.desktop-notification", 2)
            options.set_preference("layers.acceleration.disabled", True)  # Отключает аппаратное ускорение
            options.set_preference("gfx.webrender.force-disabled", True)  # Отключает WebRender (GPU рендеринг)
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            self.driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Браузер '{self.browser_type}' не поддерживается. Допустимые варианты: 'chrome', 'firefox'.")

        self.driver.maximize_window()
        self.driver.get(self.url)
        return self.driver

    def cleanup(self):
        """Закрывает драйвер и удаляет временную папку профиля Chrome."""
        if self.driver:
            self.driver.quit()
        if self.temp_profile:
            shutil.rmtree(self.temp_profile, ignore_errors=True)  # Удаляем временную папку