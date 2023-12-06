def run():    
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
    import json

    def translate_text(text, target_language='ru'):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def parse_setkab_go_id():
        url = "https://setkab.go.id"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Создаем пустой список для хранения данных новостей
            news_data = []
            
            # Находим все элементы с классом "card_berita"
            articles = soup.find_all('article', class_='card_berita')
            
            for article in articles:
                # Находим дату новости
                date = article.find('div', class_='date').text.strip()
                
                # Находим заголовок новости
                original_title = article.find('h2').text.strip()
                
                # Переводим заголовок на русский
                translated_title = translate_text(original_title)
                
                # Находим ссылку на новость
                link = url + article.find('a')['href']
                
                # Добавляем данные в список
                news_data.append({
                    'date': date,
                    'title': translated_title,
                    'link': link
                })

            # Сохраняем данные в JSON файл
            with open('1) Json folder/setkab.json', 'w', encoding='utf-8') as json_file:
                json.dump(news_data, json_file, ensure_ascii=False, indent=2)
            
            print("Данные успешно сохранены в setkab.json.")
        else:
            print(f"Ошибка при парсинге setkab: {response.status_code}")

    if __name__ == "__main__":
        parse_setkab_go_id()

run()