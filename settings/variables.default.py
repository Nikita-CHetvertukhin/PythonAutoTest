
'''Стандартные константы для тестов'''

# url адрес тестируемой сборки (по умолчанию локальный, при использовании docker вместо localhost следует указать host.docker.internal)
URL = 'http://localhost:9080/'
# Логин УЗ Администартора
ADMIN_LOGIN = 'admin'
# Пароль от УЗ администратора
ADMIN_PASSWORD = '11111111'
# MD5 от пароля администратора
ADMIN_PASSWORD_MD5 = '11111111111111111111111111111111'
# Логин от УЗ Эксперта
EXPERT_LOGIN = 'expert'
# Пароль от УЗ Эксперта
EXPERT_PASSWORD = '11111111'
# Логин первой тестовой УЗ
USER1_LOGIN = 'user1'
# Пароль от первой тестовой УЗ
USER1_PASSWORD = '11111111'

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