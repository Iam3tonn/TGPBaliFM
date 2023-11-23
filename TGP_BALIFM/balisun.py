def run():
    import re
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator
    import datetime
    import pytz

    # Function to extract article details from the article page
    def get_article_details(article_url):
        article_response = requests.get(article_url)
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            # Extracting description, publication date, and all text content
            description_element = article_soup.find('meta', property='og:description')
            description = description_element['content'] if description_element else ''

            date_element = article_soup.find('meta', property='article:published_time')
            date_published = date_element['content'] if date_element else ''

            # Convert date to a more user-friendly format
            formatted_date = ''
            if date_published:
                # Parse the ISO 8601 date string
                datetime_obj = datetime.datetime.fromisoformat(date_published)

                # Convert to a specific timezone (for example, UTC)
                utc_timezone = pytz.timezone('UTC')
                datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.utc)

                # Convert to a user-friendly string format
                formatted_date = datetime_obj_utc.astimezone(utc_timezone).strftime('%Y-%m-%d %H:%M')

            # Extract all text content from the article page
            article_text = ' '.join([p.get_text() for p in article_soup.find_all('p')])

            # Remove specific pattern
            pattern_to_remove = "Posted on Published: [^\n]+"
            article_text = re.sub(pattern_to_remove, '', article_text)

            # Remove the specified string
            article_text = article_text.replace("\n\t\tShare The Article\t", "")

            # Remove text starting from "Book The Best"
            start_index = article_text.find("Book The Best")
            if start_index != -1:
                article_text = article_text[:start_index]

            return {'description': description, 'date': formatted_date, 'text_content': article_text}
        else:
            print(f'Error accessing article page: {article_url}')
            return {'description': '', 'date_published': '', 'text_content': ''}

    # URL страницы, которую вы хотите спарсить
    url = 'https://thebalisun.com'

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

                # Переводим заголовок с английского на русский
                translated_title = translator.translate(title, src='en', dest='ru').text

                link = article.find('a')['href']

                # Get additional details from the article page
                article_details = get_article_details(link)

                # Remove the first character from text_content
                article_details['text_content'] = article_details['text_content'][1:]

                # Переводим description с английского на русский
                translated_description = translator.translate(article_details['description'], src='en', dest='ru').text

                # Переводим text_content с английского на русский
                #
                # ->###translated_text_content = translator.translate(article_details['text_content'], src='en', dest='ru').text

                # Append details to the news_items list
                news_items.append({'title': translated_title, 'link': link,
                                   'description': translated_description,
                                   'date': article_details['date'],
                                   'text_content': article_details['text_content']})

        # Записать данные в JSON-файл
        with open('1) Json folder/balisun.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_items, json_file, ensure_ascii=False, indent=4)

        print('Данные успешно записаны balisun')
    else:
        print('Ошибка при выполнении запроса к странице')

# Run the function
run()