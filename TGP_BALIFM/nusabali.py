def run():
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    from datetime import datetime
    import json

    def get_news(url):
        # Headers to simulate a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Send a request to the website with the custom headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an error for bad status

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all news items within the article-list
        news_items = soup.find('div', id='article-list').find_all('div', class_='row feature-items')

        # List to hold news data
        news_list = []

        # Create a translator object
        translator = Translator()

        for item in news_items:
            # Extract the title and link
            title_tag = item.find('h5').find('a')
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            
            # Translate the title from Indonesian to Russian
            translated_title = translator.translate(title, src='id', dest='ru').text

            # Extract and format the publication time
            time_tag = item.find('span', class_='entry-date').find('span', class_='month')
            news_time = datetime.strptime(time_tag.get_text(strip=True), '%d %b %Y %H:%M').strftime('%d %B %Y %H:%M')
            
            # Append the news information to the list
            news_list.append({'title': translated_title, 'link': link, 'time': news_time})

        return news_list

    # URL of the news page
    news_url = 'https://www.nusabali.com/'
    latest_news = get_news(news_url)

    # Save the news data to a JSON file
    with open('1) Json folder/nusabali.json', 'w', encoding='utf-8') as f:
        json.dump(latest_news, f, ensure_ascii=False, indent=4)
        print("nusabali completed")

run()