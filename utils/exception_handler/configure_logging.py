import logging
import logging.config
import os
import yaml

LOG_CONFIG_FILE = "logging_config.yaml"
LOG_DIR = "log"

# Создаём папку для логов, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

# Определяем ID воркера для уникальных логов
WORKER_ID = os.getenv('PYTEST_XDIST_WORKER', 'master')  # Получаем ID воркера ('gw0', 'gw1', 'master' и т.д.)
LOG_FILE = os.path.join(LOG_DIR, f"project_{WORKER_ID}.log")  # Каждый воркер получает уникальный файл

# Конфигурация логирования
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Позволяет избежать конфликта с уже существующими логгерами

    # Определение форматов логов
    "formatters": {
        "detailed": {  # Подробный формат логов с информацией о файле и строке кода
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        },
        "simple": {  # Упрощенный формат логов
            "format": "%(levelname)s - %(message)s"
        },
    },

    # Определение обработчиков логов
    "handlers": {
        "file": {  # Логирование в файл с ротацией (ограничение размера файла)
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",  # Записывает все сообщения уровня DEBUG и выше
            "formatter": "detailed",  # Использует подробный формат логирования
            "filename": str(LOG_FILE),  # Файл для записи логов
            "maxBytes": 5_000_000,  # Максимальный размер файла логов перед ротацией (~5MB)
            "backupCount": 5,  # Хранение 5 архивных копий логов
            "encoding": "utf-8",  # Кодировка файла логов
        },
        "console": {  # Логирование в консоль
            "class": "logging.StreamHandler",
            "level": "ERROR",  # Выводит только ошибки (ERROR и выше)
            "formatter": "simple",  # Использует упрощенный формат
            "stream": "ext://sys.stdout",  # Вывод логов в стандартный поток stdout
        },
    },

    # Корневой логгер, который применяется ко всем логгерам
    "root": {
        "level": "INFO",  # Записывает все сообщения уровня INFO и выше
        "handlers": ["file", "console"]  # Использует обработчики для записи логов в файл и консоль
    }
}

def configure_logging():
    """Настроить логирование с разделением логов по воркерам."""
    if os.path.exists(LOG_CONFIG_FILE):
        try:
            with open(LOG_CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)
                config["handlers"]["file"]["filename"] = LOG_FILE  # Устанавливаем уникальный лог-файл
                logging.config.dictConfig(config)
        except yaml.YAMLError as e:
            print(f"Ошибка загрузки YAML-конфига: {e}. Используем стандартную конфигурацию.")
            logging.config.dictConfig(LOGGING_CONFIG)
    else:
        logging.config.dictConfig(LOGGING_CONFIG)
    
    return logging.getLogger(__name__)
