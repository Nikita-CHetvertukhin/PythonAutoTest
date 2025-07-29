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

echo "[ENTRYPOINT] Запускаю prepare..."
pytest -m prepare --browser "$BROWSER"

echo "[ENTRYPOINT] Запускаю тесты: ${ARGS[*]}"
pytest "${ARGS[@]}" --browser "$BROWSER"

echo "Тесты завершены. Формирую отчёт Allure..."

# Генерация статического отчёта Allure
allure generate allure_results -o allure_report --clean

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

echo "Копирую отчёт и логи в ${report_dir}..."
mkdir -p "${report_dir}"
cp -r /app/allure_report "${report_dir}/allure_report"
cp -r /app/log "${report_dir}/logs"
cp -r /app/resources/downloads "${report_dir}/downloads"

echo "Отчёты, логи и загрузки скопированы в ${report_dir}."
