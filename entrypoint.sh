#!/bin/bash

# Запуск тестов
export PYTHONPATH=/app

BROWSER=""
ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --browser)
      BROWSER="$2"
      shift 2
      ;;
    --browser=*)
      BROWSER="${1#--browser=}"
      shift
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

echo "[ENTRYPOINT] Браузер: $BROWSER"
echo "[ENTRYPOINT] Аргументы для тестов: ${ARGS[*]}"

# Чистим allure_results один раз за весь докер-прогон (до prepare), чтобы:
# - тренд Allure строился по одному прогону, а не по смеси из прошлых запусков;
# - environment.properties, который пишет prepare, не затирался вторым вызовом pytest
rm -rf /app/allure_results/*
mkdir -p /app/allure_results

echo "[ENTRYPOINT] Запускаю prepare..."
pytest -m prepare --browser "$BROWSER"

echo "[ENTRYPOINT] Запускаю тесты: ${ARGS[*]}"
pytest "${ARGS[@]}" --browser "$BROWSER"

echo "Тесты завершены. Запрашиваю обновление отчёта Allure..."

# Результаты уже лежат в общем volume allure_results — просим сервис allure-docker-service
# пересобрать отчёт сразу, не дожидаясь опроса по таймеру
curl -s -o /dev/null -w "%{http_code}" "http://allure:5050/allure-docker-service/generate-report?project_id=doczilla-pro" \
    | { read -r code; if [ "$code" = "200" ]; then
            echo "Отчёт Allure обновлён: http://localhost:5050/allure-docker-service/projects/doczilla-pro/reports/latest/index.html"
        else
            echo "[WARN] Не удалось обновить отчёт Allure (HTTP $code) — проверьте, что контейнер allure запущен"
        fi; }
