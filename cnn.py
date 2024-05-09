def run():
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    import json

    def translate_to_russian(text):
        translator = Translator()
        translation = translator.translate(text, dest='ru')
        return translation.text if translation.text else text

    def extract_date_from_article_page(article_url):
        # Словарь для соответствия сокращенных форм месяцев и их полных названий
        month_mapping = {
            'Jan': 'January',
            'Feb': 'February',
            'Mar': 'March',
            'Apr': 'April',
            'Mei': 'May',
            'Jun': 'June',
            'Jul': 'July',
            'Agu': 'August',
            'Sep': 'September',
            'Okt': 'October',
            'Des': 'December'
        }

        response = requests.get(article_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            date_element = soup.find('div', class_='text-cnn_grey text-sm mb-4')
            if date_element:
                # Извлечь дату и время из элемента
                date_text = date_element.text.strip().split(' ', 1)[1].rsplit(' ', 1)[0]

                # Заменить сокращенные формы месяцев на полные названия
                for month_short, month_full in month_mapping.items():
                    date_text = date_text.replace(month_short, month_full)

                return date_text
        return None


    url = 'https://www.cnnindonesia.com'
    # Increase the timeout value to a larger value (e.g., 10 seconds)
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Найти нужные элементы с помощью селекторов
        news_elements = soup.select('.flex.flex-col.gap-5.nhl-list article.flex-grow')

        news_list = []

        for news_element in news_elements:
            # Извлечь данные из каждого элемента
            title_element = news_element.find('h2')
            if title_element:
                title = title_element.text.strip()
                translated_title = translate_to_russian(title)
                link = news_element.find('a')['href']

                # Получить дату публикации с отдельной страницы
                date = extract_date_from_article_page(link)

                # Check if the date is not None before saving
                if date is not None:
                    news_data = {
                        'title': translated_title,
                        'link': link,
                        'date': date
                    }

                    news_list.append(news_data)

        # Сохранить в JSON файл
        with open('1) Json folder/cnn.json', 'w', encoding='utf-8') as json_file:
            print("Данные успешно записаны в cnn.json")
            json.dump(news_list, json_file, ensure_ascii=False, indent=2)
    else:
        print(f'Ошибка парсинга cnn.json: {response.status_code}')

run()
