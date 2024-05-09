from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
import json
from googletrans import Translator

def get_full_text(article_url, translator):
    # Send GET request to the article page
    article_response = requests.get(article_url)
    
    # Check if the request was successful
    if article_response.status_code == 200:
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Find and extract the full text (assuming it's in a <div> with class 'entry-media')
        full_text_element = article_soup.find('div', class_='penci-entry-content entry-content')

        if full_text_element:
            full_text = full_text_element.get_text(strip=True)

            # Translate the full text to Russian
            translated_full_text = translator.translate(full_text, src='en', dest='ru').text
            return translated_full_text

    return None


def run():
    url = 'https://indonesiaexpat.id/news/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        translator = Translator()
        current_date = datetime.now(pytz.utc)

        # Set the target timezone (Moscow time - UTC+3)
        target_timezone = pytz.timezone('Europe/Moscow')

        for article in soup.find_all('article'):
            title_element = article.find('h2')
            date_element = article.find('time')

            if title_element and date_element:
                title = title_element.text.strip()
                link = article.find('a')['href']
                pub_date_str = date_element['datetime']
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S%z")
                
                # Convert the publication date to the target timezone
                pub_date = pub_date.astimezone(target_timezone)

                if current_date - pub_date <= timedelta(days=7):
                    translated_title = translator.translate(title, src='en', dest='ru').text

                    # Get the full text of the article and translate it to Russian
                    full_text = get_full_text(link, translator)

                    if full_text:
                        # Update the date format to the desired one
                        news_items.append({'title': translated_title, 'link': link, 'date': pub_date.strftime("%d %B %Y %H:%M"), 'text_content': full_text})
                    else:
                        print(f"Failed to retrieve full text for {title}")

        with open('1) Json folder/expat.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_items, json_file, ensure_ascii=False, indent=4)

        print('Данные успешно записаны expat')
    else:
        print('Ошибка при выполнении запроса к странице')

if __name__ == "__main__":
    translator = Translator()
    run()
