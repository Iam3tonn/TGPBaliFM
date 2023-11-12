import json
import os
import time
import balisun
import deitk
import expat
import google_bali_en, google_bali_ru, google_news_indonesia

def main():
    # Замеряем время выполнения
    start_time = time.time()

    # Запуск первого Python-скрипта
    print("Выполнение balisun.py")
    balisun.run()
    print(" ")

    # Запуск второго Python-скрипта
    print("Выполнение detik.py")
    deitk.run()
    print(" ")

    # Запуск третьего Python-скрипта
    print("Выполнение expat.py")
    expat.run()
    print(" ")

    # Запуск четвертого Python-скрипта
    print("Выполнение google_bali_en.py")
    google_bali_en.run()
    print(" ")

    # Запуск пятого Python-скрипта
    print("Выполнение google_bali_ru.py")
    google_bali_ru.run()
    print(" ")

    # Запуск шестого Python-скрипта
    print("Выполнение google_news_indonesia.py")
    google_news_indonesia.run()
    print(" ")

    # Папка, в которой находятся JSON файлы
    input_folder = "1) Json folder"
    output_file = "combined_data.json"

    # Список для хранения уникальных данных
    unique_data = []

    # Список названий, которые не должны быть объединены
    exclude_titles = ["Джембрана", "Бангли", "Национальный", "Клунгкунг", "Карангасом", "Денпасар", "Региональный", "Badung"]

    # Перебираем все файлы в папке
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            # Открываем JSON файл и читаем данные
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

                # Проверяем каждую запись и добавляем ее в список, если заголовок не находится в исключенных заголовках
                for item in data:
                    title = item.get("title")
                    if title and title not in [d.get("title") for d in unique_data] and title not in exclude_titles:
                        unique_data.append(item)

    # Сохраняем уникальные данные в итоговый JSON файл
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(unique_data, json_file, ensure_ascii=False, indent=4)

    # Завершаем замер времени выполнения
    end_time = time.time()
    execution_time = end_time - start_time

    print("Данные объединены в", output_file)
    print(f"Время выполнения программы: {execution_time:.2f} секунд")

if __name__ == "__main__":
    main()
