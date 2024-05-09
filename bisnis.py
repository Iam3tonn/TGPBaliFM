def run():
    import requests
    import json
    from bs4 import BeautifulSoup
    from googletrans import Translator

    def remove_day_from_date(date_string):
        # Удаляем название дня недели и знак "|" из строки
        date_string = date_string.replace("Selasa,", "").replace("|", "").strip()
        
        # Удаляем любое первое слово вместе с запятой
        if ',' in date_string:
            date_string = date_string.split(',', 1)[1].strip()

        return date_string

    def translate_to_russian(text):
        # Переводим текст на русский язык
        translator = Translator()
        translation = translator.translate(text, dest='ru')
        return translation.text

    url = "https://bisnis.com"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Попробуем найти блок с классом "list-news"
        news_block = soup.find('div', class_='list-news')
        
        # Если блок не найден, попробуем найти заголовки новостей напрямую
        if not news_block:
            news_titles = soup.find_all('h2')
        else:
            # Находим все заголовки новостей внутри блока
            news_titles = news_block.find_all('h2')

        news_list = []
        for title in news_titles:
            # Проверяем, есть ли тег 'a' в заголовке
            news_link_tag = title.find('a')
            if news_link_tag:
                # Получаем ссылку на новость
                news_link = news_link_tag['href']

                # Переходим на страницу новости
                news_response = requests.get(news_link)
                if news_response.status_code == 200:
                    news_soup = BeautifulSoup(news_response.text, 'html.parser')

                    # Извлекаем дату из элемента с классом "detailsAttributeDates"
                    date_element = news_soup.find('div', class_='detailsAttributeDates')
                    if date_element:
                        news_date = remove_day_from_date(date_element.get_text(strip=True))

                        # Получаем текст заголовка новости
                        news_text = translate_to_russian(news_link_tag.get_text(strip=True))

                        # Добавляем данные в список
                        news_list.append({
                            "title": news_text,
                            "link": news_link,
                            "date": news_date
                        })

        # Записываем данные в JSON файл
        with open("1) Json folder/bisnis.json", "w", encoding="utf-8") as json_file:
            json.dump(news_list, json_file, ensure_ascii=False, indent=2)

        print("Данные успешно записаны в файл bisnis.json")
    else:
        print(f"Ошибка: {response.status_code}")

run()