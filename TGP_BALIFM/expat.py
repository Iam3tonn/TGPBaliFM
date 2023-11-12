def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator

    # URL страницы, которую вы хотите спарсить
    url = 'https://indonesiaexpat.id/news/'

    # Отправить GET-запрос к странице
    response = requests.get(url)

    # Проверить успешность запроса
    if response.status_code == 200:
        # Инициализировать объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Найти все заголовки новостей и их ссылки
        news_items = []
        translator = Translator()
        for article in soup.find_all('article'):
            title_element = article.find('h2')
            if title_element:
                title = title_element.text.strip()
                link = article.find('a')['href']
                
                # Переводим заголовок с английского на русский
                translated_title = translator.translate(title, src='en', dest='ru').text
                
                news_items.append({'title': translated_title, 'link': link})

        # Записать данные в JSON-файл
        with open('1) Json folder/expat.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_items, json_file, ensure_ascii=False, indent=4)

        print('Данные успешно записаны expat')
    else:
        print('Ошибка при выполнении запроса к странице')
