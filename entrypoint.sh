#!/bin/bash
# Извлекаю URL как строку для формирвоания названия отчета в самом начале из-за особенностей BASH
url_clean="$(echo "${TEST_URL%/}" | sed -E 's|^https?://||' | tr -c '[:alnum:]' '_' | tr -s '_')"

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

filtered_args=()
for arg in "${ARGS[@]}"; do
  [[ "$arg" == -* ]] && continue  # пропускаем флаги
  filtered_args+=("$arg")
done

args_str="${filtered_args[*]}"
args_str="${args_str// /_}"  # пробелы → _

# Автоматическое копирование отчётов и логов в отдельную папку с отметкой времени
timestamp=$(date +%Y%m%d_%H%M%S)
report_dir="/app/report/${args_str}_${url_clean}_$timestamp"

echo "Копирую логи и загрузки в ${report_dir}..."
mkdir -p "${report_dir}"
cp -r /app/log "${report_dir}/logs"
cp -r /app/resources/downloads "${report_dir}/downloads"

echo "Логи и загрузки скопированы в ${report_dir}. Отчёт Allure смотрите на http://localhost:5050"
