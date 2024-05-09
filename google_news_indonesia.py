def is_family_friendly(content):
    # Add your logic to determine if the content is family-friendly
    return True

def run():
    import requests
    import json
    from datetime import datetime, timedelta
    api_key = 'e97f4805985548a0aa33fe683435e44b'
    topic = 'Индонезия'
    language = 'ru'
    page_size = 10
    api_url = f'https://newsapi.org/v2/everything?q={topic}&pageSize={page_size}&language={language}&apiKey={api_key}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        if articles:
            translated_articles = []

            # Set the current date
            current_date = datetime.now()

            for article in articles:
                # Extract the publication date of the article
                published_at = article.get('publishedAt', '')

                # Convert the published date string to a datetime object
                published_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')

                # Check if the article is published within the last week and is family-friendly
                if current_date - published_date < timedelta(days=7) and is_family_friendly(article):
                    title = article.get('title', '')
                    link = article.get('url', '')

                    # Format the publication date in a user-friendly way
                    #formatted_date = published_date.strftime('%Y-%m-%d %H:%M:%S')
                    formatted_date = published_date.strftime('%d %B %Y %H:%M')

                    # Include the formatted date in the result
                    translated_articles.append({'title': title, 'link': link, 'date': formatted_date})

            # Write the results to a JSON file
            with open('1) Json folder/google_indonesia_en.json', 'w', encoding='utf-8') as json_file:
                json.dump(translated_articles, json_file, ensure_ascii=False, indent=4)

            print(f'Saved {len(translated_articles)} family-friendly news articles from google_indonesia within the last week.')
        else:
            print('No news articles found for the query.')
    else:
        print('Error executing the request.')
        print(response.status_code)

if __name__ == "__main__":
    run()
