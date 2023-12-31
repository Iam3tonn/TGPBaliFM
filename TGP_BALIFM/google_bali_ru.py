from datetime import datetime, timedelta

def run():
    import requests
    import json

    api_key = 'e97f4805985548a0aa33fe683435e44b'
    topic = 'Бали'
    language = 'ru'
    page_size = 10

    # Вычисляем дату, которая была неделю назад от текущей даты
    one_week_ago = datetime.now() - timedelta(days=7)
    formatted_date = one_week_ago.strftime('%Y-%m-%d')

    api_url = f'https://newsapi.org/v2/everything?q={topic}&pageSize={page_size}&language={language}&apiKey={api_key}&from={formatted_date}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        if articles:
            translated_articles = []

            for article in articles:
                title = article.get('title', '')
                link = article.get('url', '')
                published_at = article.get('publishedAt', '')  # Get the publication date

                # Format the date in a user-friendly way
                formatted_published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').strftime('%d %B %Y %H:%M')

                # Append the article information to the list
                translated_articles.append({'title': title, 'link': link, 'date': formatted_published_at})

            # Save the information to the JSON file
            with open('1) Json folder/google_bali_ru.json', 'w', encoding='utf-8') as json_file:
                json.dump(translated_articles, json_file, ensure_ascii=False, indent=4)

            print(f'Сохранено {len(articles)} новостей google_bali_ru за последнюю неделю')
        else:
            print('Нет новостей по запросу за последнюю неделю.')
    else:
        print('Произошла ошибка при выполнении запроса.')
        print(response.status_code)

if __name__ == "__main__":
    run()
