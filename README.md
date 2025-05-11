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

  Глобальные переменные динамически указываются в файле `settings/variables.py`.
</details>

<details>
  <summary>✅ Запускаем чекинг лицензий и параллельную проверку доступности сборки, авторизации с логированием в единый файл "check_url.log"</summary>

  ```bash
pytest tests/check_url -n auto --alluredir=allure_results & type log\project_*.log > log\check_url.log && del log\project_*.log
  ```
</details>

<details>
  <summary>⚡ Запускаем параллельную проверку остальных тестов (чем больше потоков тем не стабильнее тесты из ФС и вебсокетов, оптимальное значение -n 3)</summary>

  ```bash
  pytest -n 3 --dist=loadscope --alluredir=allure_results --ignore=tests/check_url & type log\project_*.log > log\tests.log && del log\project_*.log
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
<summary>🚀 Выполнить билд контейнера</summary> 

```bash  
docker build -t python-auto-test .
```
</details> 

<details>
<summary>🔍 Проверить конфигурацию тестов</summary>
Конфигурация тестов задается в файле `entrypoint.sh` под комментарием `"Запуск основной последовательности тестов"`.
</details>

<details><summary>✅ Запустить контейнер с тестами, например (docker run --rm -it -p 6080:6080 -p 8080:8080 -v "D:/Dev/Auto_Test_DZ/allure_reports:/app/report" python-auto-test)</summary>

```bash
docker run --rm -it -p 6080:6080 -p 8080:8080 -v "полный_путь_до_папки_проекта_на_машине_хосте/allure_reports:/app/allure_report" python-auto-test
```
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

