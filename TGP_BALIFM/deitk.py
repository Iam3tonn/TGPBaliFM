def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator

    def get_article_text(article_url):
        response = requests.get(article_url)
        if response.status_code == 200:
            article_soup = BeautifulSoup(response.text, 'html.parser')
            article_text_element = article_soup.find('div', class_='detail__body-text')
            date_element = article_soup.find('div', class_='detail__date')  # New line to extract date

            return article_text_element.text if article_text_element else None, date_element.text if date_element else None
        else:
            print(f'Error fetching article content from {article_url}')
            return None, None

    def process_date(date_str):
        # Remove the first word before the comma and the word "WIB"
        date_parts = date_str.split(',')
        if len(date_parts) > 1:
            return ','.join(date_parts[1:]).replace('WIB', '').strip()
        return date_str

    url = 'https://www.detik.com/bali/berita'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        translator = Translator()

        for article in soup.find_all('article'):
            title_element = article.find('h2')
            if title_element:
                title = title_element.text
                link = article.find('a')['href']

                # Check if the title is one of the specified titles
                specified_titles = ["Regional", "Bangli", "Nasional", "Klungkung", "Karangasem", "Denpasar", "Badung", "Klungkung"]
                if title in specified_titles:
                    detail_title_element = article.find('div', class_='h1.detail__title')
                    if detail_title_element:
                        title = detail_title_element.text

                # Translate the title from Indonesian to Russian
                translated_title = translator.translate(title, src='id', dest='ru').text

                # Get the full text and date from the article page
                article_text, article_date = get_article_text(link)

                # Remove "\nSimak Video" and specified advertisement content
                if article_text:
                    article_text = article_text.replace("\nSimak Video", "").replace("\n\n\r\nADVERTISEMENT\r\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\r\nSCROLL TO CONTINUE WITH CONTENT\r\n\n", "")

                    # Remove any combination of \r, \t, \n from the description
                    article_text = article_text.replace("\r", "").replace("\t", "").replace("\n", "")

                # Process and format the date
                formatted_date = process_date(article_date)

                news_items.append({'title': translated_title, 'link': link, 'description': article_text, 'date': formatted_date})

        with open('1) Json folder/detik.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_items, json_file, ensure_ascii=False, indent=4)

        print('Data successfully saved in detik.json')
    else:
        print('Error making a request to the page')

run()
