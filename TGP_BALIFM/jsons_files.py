import json
import os
import time
import balisun
import deitk
import expat
import google_bali_en, google_bali_ru, google_news_indonesia
#новенькие
import bisnis, cnbc, cnn, jawapos, setkab, infodenpasar

family_friendly = [
                   "погибли", "погаорели", "арест", "суд", "тюрьму", "тюрьма", "гениталии", "гениталия", "половой", "интимный", "интинмая", "половым",
                   "криминал", "преступность", "убийство", "преступность", "преступная", "мертвый", "мертвыми", "эрекции", "пенис", "насилии", "насилие",
                   "бомбардировщик", "приступности", "наркотики", "наркотиках", "наркотикам", "погибли", "погибла", "погиб", "мертвая", "мертвым", "незаконной",
                   "госпитализирована","госпитализированы", "госпитализирован", "изнасиловали", "изнасиловал", "казахстанском", "бомбардировщик", "умер", "умерли",
                   "умерла", "ограбили", "ограбил", "ограбила", "Сан-Франциско", "секс", "сексом", "смерти", "изнасиловано", "убит", "убита", "убиты", "самоубийства",
                   "самоубийство", "убил", "убила", "убило", "несчастные", "несчастный", "убийства", "члена", "ХАМАС", "газа", "газе", "газу", " война", "войну",
                   "войны", "covid", "прогноз погоды", "премьер-лига", "расписание", "билетов", "оружие", "хакер", "гороскоп", "зодиака", "зодиак", "молитвенный",
                   "партия", "вакансии", "преступники", "обстрел", "выстрел", "лига", "вакансий", "авария", "загорелся", "Израиль", "политика", "палестина",
                   "вирус", "акции", "военные", "футбол", "безработица", "Шот муляни", "грабеж", "жертвы", "Сектор Газа", "прогноз погоды", "лига", "Shopee",
                   "похоронен", "похоронны", "заключенные", "шпион", "нефтяные резервы", "инфляция", "скидки", "беженцы", "Ливерпуль", "ВИЧ", "СПИД", "трансмарт",
                   "transmart", "фанат", "проституция", "нападающий", "сборная", "теннис", "палестина", "газы", "лига чемпионов"
                   ]
def is_family_friendly(title):
    return any(word.lower() in title.lower() for word in family_friendly)

def main():
    # Замеряем время выполнения
    start_time = time.time()

    scripts_to_run = [
        balisun.run,
        deitk.run,
        expat.run,
        google_bali_en.run,
        google_bali_ru.run,
        google_news_indonesia.run, # новенькие
        bisnis.run,
        cnbc.run,
        cnn.run,
        jawapos.run,
        setkab.run,
        infodenpasar.run
    ]

    for script in scripts_to_run:
        print(f"Выполнение {script.__name__}.py")
        try:
            script()
        except Exception as e:
            print(f"Ошибка при выполнении {script.__name__}.py: {e}")
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
                        # Проверяем, что заголовок не содержит слова из family_friendly
                        if not is_family_friendly(title):
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
