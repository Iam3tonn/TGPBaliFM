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

        # Find all news items
        news_items = soup.find_all('li', class_='p1520 art-list pos_rel')

        # List to hold news data
        news_list = []

        # Create a translator object
        translator = Translator()

        for item in news_items:
            title_tag = item.find('h3')
            if title_tag and title_tag.a:
                # Extract and translate the title from Indonesian to Russian
                original_title = title_tag.a.get_text(strip=True)
                translated_title = translator.translate(original_title, src='id', dest='ru').text
                link = title_tag.a['href']
                # Time extraction and formatting
                time_tag = item.find('time', class_='foot timeago')
                if time_tag:
                    # Adjust the datetime format here to match the actual date format
                    news_time = datetime.strptime(time_tag['title'], '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y %H:%M')
                else:
                    news_time = 'Time not available'
                # Append the news information to the list
                news_list.append({'title': translated_title, 'link': link, 'time': news_time})

        return news_list

    # URL of the news page
    news_url = 'https://bali.tribunnews.com/news'
    latest_news = get_news(news_url)


    # Save the news data to a JSON file
    with open('1) Json folder/tribunnews.json', 'w', encoding='utf-8') as f:
        json.dump(latest_news, f, ensure_ascii=False, indent=4)
        print("tribunnews completed")
run()