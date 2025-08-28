# PythonAutoTest
Автоматизация тестирования на Python с `selenium`, `pytest`, `pytest-xdist`, `Allure`.  

---

## 🔧 Установка  
Перед началом работы необходимо выполнить следующие шаги:  

<details>
  <summary>🛠️ Установить Allure</summary>

  Только для запуска тестов локально. В контейнере Allure сам генерирует отчеты
  [Документация по установке Allure](https://allurereport.org/docs/install-for-windows/)
</details>

<details>
  <summary>⚙️ Создать виртуальное окружение</summary>

  ```bash
  pip install -r requirements.txt
  ```
</details>

---

## 🚀 Запуск тестов  
Описание действий, которые необходимо выполнить для запуска проекта.

<details>
  <summary>📌 Установить путь корня проекта</summary>

  ```bash
  set PYTHONPATH=.
  ```
</details>

<details>

  <summary>📊 Указываем глобальные переменные</summary>

  Глобальные переменные динамически указываются в файле `settings/variables.py`. Перед запуском проекта нужно переименовать убрав '.default'.
</details>

<details>
  <summary>✅ Запускаем чекинг лицензий и параллельную проверку доступности сборки, авторизации, генерации схемы с логированием в единый файл" <br>
  <u>--browser</u> (по умолчанию chrome, если не указан) поддерживает аргументы <strong>chrome</strong>, <strong>firefox</strong>, <strong>edge</strong>, <strong>all</strong> или комбинацию, например <strong>edge,firefox</strong></summary>

  ```bash
pytest -m prepare --browser chrome
  ```
</details>

<details>
  <summary>⚡ Запуск тестов:<br>
  <u>--browser</u> (по умолчанию chrome, если не указан) поддерживает аргументы <strong>chrome</strong>, <strong>firefox</strong>, <strong>edge</strong>, <strong>all</strong> или комбинацию, например <strong>edge,firefox</strong></summary>

  ```bash
  pytest -m workflow_smoke --browser chrome
  ```
  ```bash
  pytest -m workflow --browser chrome
  ```
  ```bash
  pytest -m base_smoke --browser chrome
  ```
  ```bash
  pytest -m base --browser chrome
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

<details>
  <summary> ℹ️ Если работаем локально можно почистить все скрины, логи, загрузки после просмотра/сохранения отчетов</summary>

  ```bash
  python utils/cleaner.py --retention previous
  ```
</details>

---

## 🐳 Использование Docker  
Если требуется запустить тесты в контейнере, выполните следующие шаги:

<details>  
<summary>📌 Установить и запустить Docker Desktop</summary>

[Документация по установке Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
</details>  

<details>  
<summary>⚙️ Настроить файл `docker-compose.yml`:</summary>

- Если тестируем локально развернутое приложение, заменить URL в TEST_URL с http://localhost:9080/ на:
```bash
http://host.docker.internal:9080/
```
- Установить путь копирования отчета из контейнера на хост машину, например:
```bash
- "D:\\Dev\\Auto_Test_DZ\\allure_reports:/app/report"
```
</details>  

<details>  
<summary>🚀 Выполнить билд контейнера</summary> 

```bash  
docker build -t dz_autotest .
```
</details> 

<details><summary>✅ Запустить контейнер с тестами:</summary>

Аргументы -m и --browser те же, что и при запуске тестов локально
```bash
docker compose run --rm dz_autotest -m workflow_smoke --browser chrome
```
```bash
docker compose run --rm dz_autotest -m workflow --browser chrome
```
```bash
docker compose run --rm dz_autotest -m base_smoke --browser chrome
```
```bash
docker compose run --rm dz_autotest -m base --browser chrome
```

</details>

<details>
  <summary>🌍 Просмотреть отчет Allure</summary>

  **На машину хост отчёт Allure и текстовые логи сохраняются по пути указанном в volumes файла docker-compose.yml (установленный Allure для просмотра готового отчета не нужен):**

  ```bash
  python -m http.server 8080
  ```
</details>

<details>
  <summary>⚡ При необходимости запустить с новыми параметрами без повторного билда:</summary>

  **Поменять ссылку на новую сборкe в docker-composs.yml и/или ввести новые аргументы в команду**

  ```bash
  docker compose run --rm dz_autotest -m workflow --browser firefox
  ```
</details>

