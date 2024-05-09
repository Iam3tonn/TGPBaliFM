def run():
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    import json

    def translate_to_russian(text):
        translator = Translator()
        translation = translator.translate(text, dest='ru')
        return translation.text

    def extract_date(news_url):
        response = requests.get(news_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            date_element = soup.find('div', class_='date')
            if date_element:
                return date_element.text.strip()
        return None

    url = 'https://www.cnbcindonesia.com'

    # Отправляем GET-запрос на сайт
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим элементы с новостями (пример)
        news_elements = soup.select('ul.list.media_rows.middle.thumb.terbaru li article')

        # Создаем список для хранения данных
        news_list = []

        # Обрабатываем найденные новости
        for news_element in news_elements:
            # Извлекаем заголовок и ссылку
            title = news_element.find('h2').text
            translated_title = translate_to_russian(title)  # Переводим заголовок на русский
            link = news_element.find('a')['href']

            # Извлекаем дату
            date = extract_date(link)

            # Пропускаем новость, если дата отсутствует
            if date is None:
                continue

            # Создаем словарь с данными новости
            news_data = {
                'title': translated_title,
                'link': f'{link}',
                'date': date
            }

            # Добавляем словарь в список
            news_list.append(news_data)

        # Записываем данные в JSON файл, только если есть новости с датами
        if news_list:
            with open('1) Json folder/cnbc.json', 'w', encoding='utf-8') as json_file:
                json.dump(news_list, json_file, ensure_ascii=False, indent=2)

            print('Данные успешно загружены в cnbc.json.')
        else:
            print('Новых новостей для cnbc не найдено.')

    else:
        print(f'Ошибка парсинга страницы cnbc. Status code: {response.status_code}')

run()