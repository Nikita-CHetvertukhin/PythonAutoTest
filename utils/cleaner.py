import os
import argparse
from datetime import datetime, timedelta

# Предопределённые директории для очистки
directories_to_clean = ["allure_results", "log/screenshots", "resources/downloads"]
exclude_paths = ["log/licence_properties.json", "allure_reports/docker_reports.gitkeep"]

def clean_old_files(retention):
    """
    Удаляет файлы, старше указанного периода, из предопределённых директорий.

    :param retention: Параметры хранения ('previous', 'day', 'week', 'month').
                      previous - удаляет все файлы, кроме исключённых.
                      day - файлы старше 1 дня.
                      week - файлы старше 1 недели.
                      month - файлы старше 1 месяца.
    """
    retention_map = {
        "day": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=30)
    }

    if retention not in retention_map and retention != "previous":
        raise ValueError(f"Неверное значение retention: {retention}. Доступные: {list(retention_map.keys()) + ['previous']}")

    threshold_date = datetime.now() - retention_map.get(retention, timedelta(days=30))  # Default: 1 Месяц

    normalized_exclude_paths = [os.path.normpath(excluded) for excluded in exclude_paths]

    for directory in directories_to_clean:
        if not os.path.exists(directory):
            continue

        for root, _, files in os.walk(directory):
            if any(os.path.commonpath([root, excluded]) == excluded for excluded in normalized_exclude_paths):
                continue

            for filename in files:
                file_path = os.path.join(root, filename)

                if os.path.relpath(file_path, start=os.getcwd()) in normalized_exclude_paths:
                    continue  # Пропускаем исключённые файлы

                if retention == "previous":  # Удаляем ВСЕ файлы, кроме исключённых
                    try:
                        os.remove(file_path)
                        print(f"Удалён файл: {file_path}")
                    except Exception as e:
                        print(f"Ошибка удаления файла {file_path}: {e}")
                else:  # Удаляем по дате модификации
                    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mod_time < threshold_date:
                        try:
                            os.remove(file_path)
                            print(f"Удалён устаревший файл: {file_path}")
                        except Exception as e:
                            print(f"Ошибка удаления файла {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Очистка устаревших файлов.")
    parser.add_argument("--retention", type=str, required=True, choices=["previous", "day", "week", "month"],
                        help="Срок хранения файлов: previous (удалить всё), day (старше 1 дня), week (старше 1 недели), month (старше 1 месяца).")
    
    args = parser.parse_args()
    clean_old_files(args.retention)