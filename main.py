
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent

file_name = input("Введите имя CSV-файла: ")

if not file_name.endswith(".csv"):
    file_name += ".csv"

input_file = BASE_DIR / "data" / file_name
output_file = BASE_DIR / "output" / f"{Path(file_name).stem}_cleaned.csv"

print("CSV Cleaner запущен!")
print("-" * 30)

if not input_file.exists():
    print(f"Ошибка: файл {input_file} не найден!")
else:
    with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise SystemExit("Ошибка! CSV-файл пуст или не содержит заголовков.")
        required_columns = {"name", "age", "city"}
        actual_columns = set(reader.fieldnames or [])
        missing_columns = required_columns - actual_columns
        if missing_columns:
            raise SystemExit(f"Ошибка! Отсутствуют столбцы: {','.join(sorted(missing_columns))}")
        rows = list(reader)
        if not rows:
            raise SystemExit("Ошибка! CSV-файл не содержит записей.")
        for row in rows:
            for key in row:
                row[key] = row[key].strip()

        before_count = len(rows)
        unique_rows = []
        seen = set()
        for row in rows:
            row_key = tuple(row.values())

            if row_key not in seen:
                seen.add(row_key)
                unique_rows.append(row)

        removed_duplicates = before_count - len(unique_rows)
        rows = unique_rows
        valid_rows = []
        for row in rows:
            try:
                age = int(row["age"])
                if age > 0:
                    valid_rows.append(row)
                else:
                    print("Некорректный возраст:", row["name"])
            except ValueError:
                print("Ошибка в возрасте:", row["name"])
        invalid_count = len(rows) - len(valid_rows)
        rows = valid_rows
        removed_count = before_count - len(rows)

        print("Удалено дубликатов:", removed_duplicates)
        print("Удалено некорректных записей:", invalid_count)
        try:
            with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print("Очищенная таблица сохранена!")
            print("Путь:", output_file)
        except OSError as error:
            print("Ошибка при сохранении файла!")
            print("Причина:", error)

    print("Столбцы:", reader.fieldnames)
    print("Количество записей:", len(rows))

    print("\nПервые три записи:")

    for row in rows[:3]:
        print(row)

print("\nПроверка завершена.")