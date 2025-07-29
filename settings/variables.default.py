import os

'''Стандартные константы для тестов'''

# URL адрес тестируемой сборки если не задан в аргументах используется прописанный вручную
# (по умолчанию локальный, при использовании docker вместо localhost следует указать host.docker.internal)
# Адрес для docker берется из TEST_URL docker-compose.yml
URL = os.getenv('TEST_URL', 'http://localhoat:9080')
# Логин УЗ Администартора
ADMIN_LOGIN = 'AQA_admin'
# Пароль от УЗ администратора
ADMIN_PASSWORD = '11111111'
# MD5 от пароля администратора
ADMIN_PASSWORD_MD5 = '11111111111111111111111111111111'
# Логин от УЗ Эксперта
EXPERT_LOGIN = 'AQA_expert'
# Пароль от УЗ Эксперта
EXPERT_PASSWORD = '11111111'
# Логин первой тестовой УЗ
USER1_LOGIN = 'AQA_user1'
# Пароль от первой тестовой УЗ
USER1_PASSWORD = '11111111'
# Логин второй тестовой УЗ
USER2_LOGIN = 'AQA_user2'
# Пароль от второй тестовой УЗ
USER2_PASSWORD = '11111111'
# Логин третьей тестовой УЗ
USER3_LOGIN = 'AQA_user3'
# Пароль от третьей тестовой УЗ
USER3_PASSWORD = '11111111'
# Логин четвертой тестовой УЗ
USER4_LOGIN = 'AQA_user4'
# Пароль от четвертой тестовой УЗ
USER4_PASSWORD = '11111111'
# Логин пятой тестовой УЗ
USER5_LOGIN = 'AQA_user5'
# Пароль от пятой тестовой УЗ
USER5_PASSWORD = '11111111'

'''API константы для тестов'''

# URL для API запросов
API_URL = f'{URL}/request.json'
# Основной компонент "Документы" сборки 
WORKSPACE = 'pro.doczilla.workflow.workspace.table.Workspace'
# Секция "Мои файлы"
MY_FILES_SECTION = '00629445-F77A-407C-9F4D-3E3B63D7DA2D'
# Секция "Шаблоны процессов"
WORKFLOWS_SECTION = 'B63284D5-A364-4211-AA8C-E518077DCEE6'

'''Патчи'''

# Файл со списокм всех лицензий и их значений по умолчанию
DEFAULT_LICENCE_FILE = "settings/default_licence_properties.json"
# Путь до файла формируемого в процессе тестов с актуальными значениями лицензий
LICENCE_OUTPUT_FILE = "log/licence_properties.json"
# Путь до файла формируемого в процессе тестов с параметрами окружения для Allure
ENV_FILE = "allure_results/environment.properties"
# Путь до папки с файлами необходимыми для тестов
UPLOADS_PATH = "resources/uploads"
# Путь до папки с профилями браузеров
PROFILES_PATH = "resources/profiles"
# Скрипт вебсокет
WEBSOCKET_PATCH = """
window.WebSocket = class {
  constructor() {
    console.warn("WebSocket блокирован: соединение не устанавливается.");
    this.readyState = 3; // CLOSED
  }
  close() {}
  send() {}
  set onopen(_) {}
  set onmessage(_) {}
  set onerror(_) {}
  set onclose(_) {}
};
"""

'''Лицензии'''

# Общие диски
SHARE_DRIVES = 'pro.doczilla.sharing.drives'