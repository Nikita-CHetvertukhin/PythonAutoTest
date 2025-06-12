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
  <summary>✅ Запускаем чекинг лицензий и параллельную проверку доступности сборки, авторизации с логированием в единый файл "check_url.log" <br>
  <u>BROWSER</u> поддерживает аргументы <strong>chrome</strong> и <strong>firefox</strong></summary>

  ```bash
set BROWSER=chrome & pytest tests/check_url -n auto --alluredir=allure_results & type log\project_*.log > log\check_url.log && del log\project_*.log
  ```
</details>

<details>
  <summary>⚡ Запускаем параллельную проверку тестов Workflow<br>
  <u>BROWSER</u> поддерживает аргументы <strong>chrome</strong> и <strong>firefox</strong></summary>

  ```bash
  set BROWSER=chrome & pytest tests/workflow -n auto --dist=loadscope --alluredir=allure_results & type log\project_*.log > log\tests.log && del log\project_*.log
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
<summary>⚙️ Настроить файл `variables.py`. Если тестируем локально развернутое приложение, заменить URL в файле `variables.py` с `http://localhost:9080/` на:</summary>

```bash
http://host.docker.internal:9080/
```
</details>  

<details>
<summary>🔍 Проверить конфигурацию тестов</summary>
Конфигурация тестов задается в файле `entrypoint.sh` под комментарием `"Запуск основной последовательности тестов"`.
</details>

<details>  
<summary>🚀 Выполнить билд контейнера</summary> 

```bash  
docker build -t python-auto-test .
```
</details> 

<details><summary>✅ Запустить контейнер с тестами:</summary>

С помощью команды, в котором аргументом -e BROWSER=chrome задаем браузер (также поддерживает firefox) например:
```bash
docker run --rm -it -e BROWSER=firefox -p 6080:6080 -p 8080:8080 -v "полный_путь_до_папки_проекта_на_машине_хосте/allure_reports:/app/allure_report" python-auto-test
```
Или через UI Docker Desktop:
1. Открыть Images и найти сбилденный образ
2. Нажать Run и открыть Optional Settings
3. По желанию ввести имя контейнера
4. Указать порт "6080" для noVNC
5. Выбрать путь до папки, в которую хотим получить отчёт (обычно папка_проекта/allure_reports)
6. Указать путь до отчета внутри контейнера "/app/report"
7. Указать переменную BROWSER со значением chrome или firefox
8. Нажать Run

![Docker UI](https://drive.google.com/uc?export=view&id=1AThlLXKHwrk-QG25dD3-Mgde9oJgV4T2)

</details>

<details>
  <summary>🌍 Просмотреть отчет Allure</summary>

  **Для отслеживания хода тестирования и просмотра результатов откройте в браузере на машине хосте:**

  ```bash
  http://localhost:6080/vnc.html
  ```

  **На машину хост отчёт Allure и текстовые логи сохраняются по пути:**

  ```bash
  полный_путь_до_папки_проекта_на_машине_хосте/allure_reports
  ```
</details>

