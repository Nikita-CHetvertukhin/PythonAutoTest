 Doczilla User Generate Script
Скрипт автоматизирует создание и настройку тестовых пользователей в системе Doczilla:

Создаёт пользователей, группу, роли и компоненты;
назначает права в зависимости от типа пользователя (admin, expert, user);
устанавливает (и при необходимости сбрасывает) пароли.


 Требования
Python 3.8+
Пакеты: requests, pyyaml, python-dotenv
Установка зависимостей:
pip install requests pyyaml python-dotenv

Структура проекта
script_auto_generate_script/
├── main.py                 # основной скрипт
├── doczilla_client.py      # клиент для работы с API Doczilla
├── config.yaml             # описание пользователей, ролей и компонентов
├── .env                    # секреты (URL, логин/пароль администратора)
└── README.md

Настройка
1. Создайте .env
DOCZILLA_URL=https://ваш-инстанс.doczilla.pro/
OWNER_LOGIN=admin
OWNER_PASSWORD=ваш_пароль_админа

2. Настройте config.yaml
users:
  - login: AQA_admin
    password: "11111111"
    type: admin
  - login: AQA_expert
    password: "11111111"
    type: expert
  - login: AQA_user1
    password: "11111111"
    type: user

role_sets:
  admin: ["User", "Пользователи", "Administrator", "Администратор"]
  expert: ["User", "Пользователи", "Expert", "Эксперт"]
  user: ["User", "Пользователи"]

entry_sets:
  admin: ["Статистика", "Справочники", ..., "Администрирование", "Настройки"]
  expert: ["Статистика", "Справочники", ..., "Workflow"]
  user: ["Статистика", "Справочники", ..., "Workflow"]

group:
  name: AQA_GROUP

Базовый запуск - python main.py
С сбросом паролей - python main.py --reset-password
С отладкой (подробные логи) - python main.py --debug
Комбинированный режим - python main.py --debug --reset-password
С кастомными файлами - python main.py --config config/staging.yaml --env .env.prod
Помощь - python main.py --help