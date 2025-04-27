import logging  # Работа с логированием
from logging.handlers import RotatingFileHandler  # Ротация логов для управления файлами
import os  # Работа с файловой системой

# Настройка логирования
def configure_logging(log_file='log/project.log'):
    """
    Настраивает логирование для проекта с выводом в файл и консоль.

    :param log_file: Путь к файлу для записи логов. Создаётся папка 'log', если её нет.
    :return: Конфигурированный логгер.
    """
    # Проверка и создание папки для логов, если она отсутствует
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Создание обработчика ротации логов (до 5 MB, 5 резервных копий)
    handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=5)

    # Создание и настройка логгера
    logger = logging.getLogger('ProjectLogger')
    logger.setLevel(logging.DEBUG)  # Уровень логирования: DEBUG

    # Формат сообщений в логах
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Добавление обработчика для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)  # Уровень логов в консоли
    logger.addHandler(console_handler)

    return logger
