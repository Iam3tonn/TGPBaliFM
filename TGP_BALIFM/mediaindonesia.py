def run():    
    import requests
    from bs4 import BeautifulSoup
    import json

    # URL сайта для парсинга
    url = "https://mediaindonesia.com/search?q=bali#gsc.tab=0&gsc.q=bali&gsc.page=1"

    # Заголовки запроса, имитирующие браузер
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
    }

    # Отправка GET-запроса на сайт с использованием заголовков
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Найдем все заголовки и ссылки на странице
        articles = soup.find_all("article")

        data = []

        for article in articles:
            # Пример выбора заголовка и ссылки
            link = article.find("a")  # Возможно, вам потребуется изменить способ выбора
            title = link.text if link else "Нет доступной информации"
            href = link.get("href") if link else ""

            data.append({"title": title, "link": href})

        # Сохранение данных в JSON файл
        with open("media_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("Данные сохранены в coconuts_data.json.")
    else:
        print("Не удалось получить доступ к сайту. Код состояния:", response.status_code)
