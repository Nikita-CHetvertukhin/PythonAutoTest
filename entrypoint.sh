#!/bin/bash
# Запуск виртуального дисплея Xvfb на дисплее :99
echo "Запуск виртуального дисплея Xvfb..."
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Запуск VNC-сервера (x11vnc) на порту 5900
echo "Запуск x11vnc-сервера..."
x11vnc -display :99 -forever -nopw -shared -rfbport 5900 &

# Запуск лёгкого оконного менеджера (fluxbox)
echo "Запуск оконного менеджера fluxbox..."
fluxbox &

# Добавляем задержку, чтобы x11vnc успел запуститься
sleep 2

# Запуск noVNC proxy для предоставления HTML5-интерфейса
echo "Запуск noVNC proxy..."
/opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

echo "Виртуальный дисплей, VNC-сервер и noVNC запущены."
echo "Подключайтесь к noVNC по адресу http://localhost:6080/vnc.html"

# Запуск основной последовательности тестов
export PYTHONPATH=/app
pytest -m prepare
pytest -m workflow
echo "Тесты завершены. Формирую отчёт Allure..."

# Генерация статического отчёта Allure
allure generate allure_results -o allure_report --clean

echo "Запуск HTTP-сервера для отчёта Allure..."
cd /app/allure_report
python3 -m http.server 8080 &
cd /app

# Автоматическое открытие браузера с Allure-отчётом с флагом --no-sandbox
echo "Автоматически запускаю браузер на http://localhost:8080..."
google-chrome --no-sandbox --new-window "http://localhost:8080" &

echo "Отчёт Allure доступен по адресу http://localhost:8080."

# Автоматическое копирование отчётов и логов в отдельную папку с отметкой времени
timestamp=$(date +%Y%m%d_%H%M%S)
report_dir="/app/report/report_$timestamp"

echo "Копирую отчёт и логи в ${report_dir}..."
mkdir -p "${report_dir}"
cp -r /app/allure_report "${report_dir}/allure_report"
cp -r /app/log "${report_dir}/logs"
cp -r /app/resources/downloads "${report_dir}/downloads"

echo "Отчёты, логи и загрузки скопированы в ${report_dir}."

echo "Контейнер остается запущенным для обзора виртуального рабочего стола."
tail -f /dev/null
