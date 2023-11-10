import requests
import json
#from googletrans import Translator  # Установите библиотеку 'googletrans==4.0.0-rc1' через pip

# Замените 'YOUR_API_KEY' на ваш API ключ
api_key = 'e97f4805985548a0aa33fe683435e44b'

# Задайте параметры запроса
topic = 'Индонезия'
language = 'ru'  # Язык новостей (например, английский)
page_size = 10  # Количество новостей, которое вы хотите получить
api_url = f'https://newsapi.org/v2/everything?q={topic}&pageSize={page_size}&language={language}&apiKey={api_key}'

# Отправьте запрос к News API
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    articles = data.get('articles', [])

    if articles:
        translated_articles = []

        # Создайте объект для перевода
        #translator = Translator()

        for article in articles:
            title = article.get('title', '')
            link = article.get('url', '')

            # Переведите заголовок с английского на русский
            #translated_title = translator.translate(title, src='en', dest='ru').text

            translated_articles.append({'title': title, 'link': link})

        # Запишите результаты в JSON файл
        with open('TGP_BALIFM/1) Json folder/google_indonesia_en.json', 'w', encoding='utf-8') as json_file:
            json.dump(translated_articles, json_file, ensure_ascii=False, indent=4)
        print(f'Сохранено {len(articles)} новостей google_indonesia')
    else:
        print('Нет новостей по запросу.')
else:
    print('Произошла ошибка при выполнении запроса.')
