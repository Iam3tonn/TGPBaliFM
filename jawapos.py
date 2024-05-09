def run():    
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    import json

    url = 'https://www.jawapos.com'

    # Устанавливаем заголовки User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Отправляем GET-запрос к сайту
    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Создаем список для хранения данных новостей
        news_list = []

        # Находим элементы с классом "col-bs10-7", "latest clearfix", "latest__wrap"
        news_elements = soup.find_all(['div'], class_=["col-bs10-7", "latest clearfix", "latest__wrap"])

        # Создаем объект для машинного перевода
        translator = Translator()

        for news_element in news_elements:
            # Создаем словарь для хранения данных каждой новости
            news_data = {}

            # Получаем ссылку на страницу новости
            link_element = news_element.find('a', href=True)
            if link_element:
                news_data['link'] = link_element['href']

            # Получаем текст новости из атрибута alt
            text_element = news_element.find('img')
            if text_element:
                news_data['News Text'] = text_element.get('alt', '')

                # Переводим текст новости на русский
                translation = translator.translate(news_data['News Text'], src='auto', dest='ru')
                news_data['title'] = translation.text

            # Получаем дату публикации новости
            date_element = news_element.find('date', class_='latest__date')
            if date_element:
                # Получаем текст даты публикации и удаляем "WIB"
                publication_date = date_element.get_text(strip=True).replace('WIB', '')
                news_data['date'] = publication_date

            # Добавляем данные новости в список
            news_list.append(news_data)

        # Сохраняем данные в JSON файл
        with open('1) Json folder/jawapos.json', 'w', encoding='utf-8') as json_file:
            print("Данные успешно записаны в jawapos.json")
            json.dump(news_list, json_file, ensure_ascii=False, indent=2)

    else:
        print('Ошибка парсинга jawapos:', response.status_code)

run()