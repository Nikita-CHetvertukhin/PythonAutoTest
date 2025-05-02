# PythonAutoTest
Автоматизация тестирования на Python с `selenium`, `pytest`, `pytest-xdist`, `Allure`.  

---

## 🔧 Установка  
Перед началом работы необходимо выполнить следующие шаги:  

<details>
  <summary>🛠️ Установить Allure</summary>

  [Документация по установке Allure](https://allurereport.org/docs/install-for-windows/)
</details>

<details>
  <summary>⚙️ Создать виртуальное окружение</summary>

  ```bash
  pip install -r requirements.txt
  ```
</details>

<details>
  <summary>📌 Установить путь корня проекта</summary>

  ```bash
  set PYTHONPATH=.
  ```
</details>

---

## 🚀 Запуск тестов  
Описание действий, которые необходимо выполнить для запуска проекта.

<details>
  <summary>📊 Указываем глобальные переменные</summary>

  Глобальные переменные динамически указываются в файле `settings/variables.py`.
</details>

<details>
  <summary>✅ Запускаем параллельную проверку доступности сборки и авторизации с логированием в единый файл "check_url.log"</summary>

  ```bash
  pytest tests/check_url -n auto --alluredir=allure_results && type log\project_*.log > log\check_url.log && del log\project_*.log
  ```
</details>

<details>
  <summary>⚡ Запускаем параллельную проверку остальных тестов</summary>

  ```bash
  pytest -n auto --dist=loadscope --alluredir=allure_results --ignore=tests/check_url && type log\project_*.log > log\tests.log && del log\project_*.log
  ```
</details>

---

## 📊 Просмотр отчетов  
Логи хранятся в папке `log`, а скриншоты ошибок — в `screenshots`.  
Для генерации отчетов используется **Allure**.

<details>
  <summary>📜 Генерируем отчет Allure в браузере</summary>

  ```bash
  allure serve allure_results
  ```
</details>

<details>
  <summary>💾 Сохранение отчета локально</summary>

  ```bash
  allure generate allure_results --clean -o allure-report
  ```
</details>

<details>
  <summary>🌍 Просмотр сохраненного отчета через локальный HTTP сервер</summary>

  ```bash
  python -m http.server 8080
  ```
</details>

---

## 🐳 Использование Docker  
Если требуется запустить тесты в контейнере, выполните следующие команды:  
```bash
docker build -t python-auto-test .
docker run --rm python-auto-test
```