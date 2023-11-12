def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator

    url = 'https://www.detik.com/bali/berita'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        translator = Translator()

        for article in soup.find_all('article'):
            title_element = article.find('h2')
            if title_element:
                title = title_element.text.strip()
                link = article.find('a')['href']

                # Check if the title is one of the specified titles
                specified_titles = ["Regional", "Bangli", "Nasional", "Klungkung", "Karangasem", "Denpasar", "Badung", "Klungkung"]
                if title in specified_titles:
                    detail_title_element = article.find('div', class_='h1.detail__title')
                    if detail_title_element:
                        title = detail_title_element.text.strip()

                # Translate the title from Indonesian to Russian
                translated_title = translator.translate(title, src='id', dest='ru').text

                news_items.append({'title': translated_title, 'link': link})

        with open('1) Json folder/detik.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_items, json_file, ensure_ascii=False, indent=4)

        print('Data successfully saved in detik.json')
    else:
        print('Error making a request to the page')
