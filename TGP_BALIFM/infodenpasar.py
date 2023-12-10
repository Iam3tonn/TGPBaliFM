def run():
    import requests
    from bs4 import BeautifulSoup
    import datetime
    import json
    from googletrans import Translator

    url = "https://www.infodenpasar.id"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы, соответствующие вашей структуре
        news_elements = soup.find_all('div', class_='td_module_column')

        data_list = []

        # Initialize the translator
        translator = Translator()

        for news_element in news_elements:
            # Получаем нужные данные из каждого элемента
            title_element = news_element.find('h3', class_='entry-title td-module-title')
            title = title_element.text.strip() if title_element else "Нет заголовка"

            # Translate the title to Russian
            translated_title = translator.translate(title, src='auto', dest='ru').text

            # Добавляем получение ссылки и даты публикации
            link = title_element.a['href'] if title_element and title_element.a else "Нет ссылки"
            date_element = news_element.find('time', class_='entry-date')
            date = date_element['datetime'] if date_element else "Нет даты"

            try:
                if date != "Нет даты":
                    datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
                    formatted_date = datetime_obj.strftime('%d %B %Y %H:%M')
                else:
                    formatted_date = "Нет даты"
            except ValueError:
                formatted_date = "Нет даты (неверный формат)"

            # Create a dictionary for each news item
            news_data = {
                "title": translated_title,
                "link": link,
                "date": formatted_date
            }

            data_list.append(news_data)

        # Save the data to a JSON file
        with open('1) Json folder/infodenpasar.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_list, json_file, ensure_ascii=False, indent=4)

        print("Данные сохранены в файл 'infodenpasar.json'.")

    else:
        print(f"Ошибка при получении страницы infodenpasar. Код статуса: {response.status_code}")

run()