# PythonAutoTest

1. Перед началом работы:
# Подтянуть фреймворки и билиотеки
pip install requirements.txt
# Установить путь корня проекта
set PYTHONPATH=.
# Установить Allure
https://allurereport.org/docs/install-for-windows/

2. Перед запуском изменить параметры в settings/variables.py

3. Запустить в консоли IDE или из консоли в ОС в папке проекта командой:
pytest --alluredir=allure-results
# Для генерации отчета Allure в файле
allure generate allure-results --clean -o allure-report
# Чтобы корректно открыть такой отчет нужно развернуть локальный http сервер python
python -m http.server 8080
Далее в браузере:
http://localhost:8080
# Для генерации отчета Allure в браузере
allure serve allure-results

*При использовании Docker выполнить следующие команды в консоли из папки с проектом:
docker build -t python-auto-test .
docker run --rm python-auto-test
