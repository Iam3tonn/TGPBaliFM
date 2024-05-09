def run():
    import time
    from datetime import datetime, timedelta
    import requests
    import json
    from googletrans import Translator  # Установите библиотеку 'googletrans==4.0.0-rc1' через pip
    import pytz

    # Замените 'YOUR_API_KEY' на ваш API ключ
    api_key = 'e97f4805985548a0aa33fe683435e44b'

    # Определите диапазон дат (в данном случае, последняя неделя)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Задайте параметры запроса
    topic = 'bali'
    language = 'en'  # Язык новостей (например, английский)
    page_size = 10  # Количество новостей, которое вы хотите получить

    # Формируйте строку с диапазоном дат для запроса
    date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

    api_url = f'https://newsapi.org/v2/everything?q={topic}&pageSize={page_size}&language={language}&apiKey={api_key}&from={date_range}'

    # Отправьте запрос к News API
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        if articles:
            translated_articles = []

            # Создайте объект для перевода
            translator = Translator()

            for article in articles:
                title = article.get('title', '')
                link = article.get('url', '')
                published_at = article.get('publishedAt', '')

                # Check if the article is within the last week
                article_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                if article_date >= start_date:
                    # Add a delay between requests to avoid 429 error
                    time.sleep(3)  # Sleep for 3 seconds

                    # Translate the title from English to Russian
                    translated_title = translator.translate(title, src='en', dest='ru').text

                    # Format the date in a user-friendly way
                    formatted_date = article_date.strftime('%d %B %Y %H:%M')

                    translated_articles.append({
                        'title': translated_title,
                        'link': link,
                        'date': formatted_date
                    })

            # Запишите результаты в JSON файл
            with open('1) Json folder/google_bali_en.json', 'w', encoding='utf-8') as json_file:
                json.dump(translated_articles, json_file, ensure_ascii=False, indent=4)
            print(f'Сохранено {len(translated_articles)} новостей google_bali_en за последнюю неделю')
        else:
            print('Нет новостей по запросу.')
    else:
        print('Произошла ошибка при выполнении запроса.')
        print(response.status_code)


if __name__ == "__main__":
    run()
