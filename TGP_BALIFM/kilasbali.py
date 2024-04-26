def run():
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    import json
    from datetime import datetime

    def translate_date(ind_date):
        # Indonesian to English month mapping
        months = {
            'Januari': 'January',
            'Februari': 'February',
            'Maret': 'March',
            'April': 'April',
            'Mei': 'May',
            'Juni': 'June',
            'Juli': 'July',
            'Agustus': 'August',
            'September': 'September',
            'Oktober': 'October',
            'November': 'November',
            'Desember': 'December'
        }
        parts = ind_date.split()
        # Example input: Rabu, 24 April 2024
        day = parts[1].strip(',')
        month = months[parts[2]]
        year = parts[3]
        # Assuming a fixed time for all entries, as time is not provided
        time = "12:00"
        formatted_date = f"{day} {month} {year} {time}"
        return formatted_date

    def get_news(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find('div', class_='mag-box-container clearfix').find_all('li', class_='post-item tie-standard')

        news_list = []
        translator = Translator()

        for item in news_items:
            title_link = item.find('h2', class_='post-title').find('a')
            title = title_link.get_text(strip=True)
            link = title_link['href']
            translated_title = translator.translate(title, src='id', dest='ru').text

            date_info = item.find('span', class_='date meta-item tie-icon')
            news_date = translate_date(date_info.get_text(strip=True)) if date_info else 'No date found'

            news_list.append({'title': translated_title, 'link': link, 'date': news_date})

        return news_list

    news_url = 'https://www.kilasbali.com/'
    latest_news = get_news(news_url)

    with open('1) Json folder/kilasbali.json', 'w', encoding='utf-8') as f:
        json.dump(latest_news, f, ensure_ascii=False, indent=4)
        print("kilasbali completed")
run()