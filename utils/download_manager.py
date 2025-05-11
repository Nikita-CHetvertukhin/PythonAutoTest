import os
import time

class DownloadManager:
    """Класс для управления загрузками файлов."""

    def __init__(self, base_dir=None):
        """
        Инициализация менеджера загрузок.
        :param base_dir: Корневая папка проекта (по умолчанию определяется автоматически)
        """
        if base_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Корень проекта
        self.download_dir = os.path.join(base_dir, "resources", "downloads")

        # Создаём папку, если её нет
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_download_path(self):
        """Возвращает путь к папке загрузок."""
        return self.download_dir

    def verify_downloaded_file(self, filename, timeout=10):
        """
        Проверяет, что файл был загружен и его размер больше 1 байта.
        
        :param filename: Имя файла (например, "process_name.dzwf")
        :param timeout: Время ожидания появления файла (по умолчанию 10 секунд)
        :return: True, если файл загружен успешно, иначе False
        """
        downloaded_file = os.path.join(self.download_dir, filename)

        # Ожидание появления файла
        while timeout > 0:
            if os.path.exists(downloaded_file):
                if os.path.getsize(downloaded_file) > 1:
                    return True  # Файл найден и не пустой
                return False  # Файл пустой
            time.sleep(1)
            timeout -= 1

        return False  # Файл не найден