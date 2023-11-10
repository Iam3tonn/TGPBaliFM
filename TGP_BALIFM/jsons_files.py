import json
import os
import subprocess
import time

# Замеряем время выполнения
start_time = time.time()

# Запуск первого Python-скрипта
print("Выполнение balisun.py")
script1 = "TGP_BALIFM/balisun/balisun.py"
subprocess.run(["python", script1])
print(" ")

# Запуск второго Python-скрипта
print("Выполнение detik.py")
script2 = "TGP_BALIFM/detik/deitk.py"
subprocess.run(["python", script2])
print(" ")

# Запуск третьего Python-скрипта
print("Выполнение expat.py")
script3 = "TGP_BALIFM/indonisea expat/expat.py"
subprocess.run(["python", script3])
print(" ")

# Запуск четвертого Python-скрипта
print("Выполнение google_bali_en.py")
script4 = "TGP_BALIFM/google_damn/google_bali_en.py"
subprocess.run(["python", script4])
print(" ")

# Запуск пятого Python-скрипта
print("Выполнение google_bali_ru.py")
script5 = "TGP_BALIFM/google_damn/google_bali_ru.py"
subprocess.run(["python", script5])
print(" ")

# Запуск шестого Python-скрипта
print("Выполнение google_bali_indonesia.py")
script6 = "TGP_BALIFM/google_damn/google_news_indonesia.py"
subprocess.run(["python", script6])
print(" ")



# Папка, в которой находятся JSON файлы
input_folder = "TGP_BALIFM/1) Json folder"
output_file = "TGP_BALIFM/combined_data.json"

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
