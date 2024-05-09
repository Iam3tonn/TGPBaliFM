def run():
    import httpx
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator

    async def fetch_data():
        # URL сайта для парсинга
        url = "https://coconuts.co/bali/news/"

        # Заголовки запроса, имитирующие браузер
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
        }

        # Создание HTTP-сессии с httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Найдем все заголовки и ссылки на странице
            articles = soup.find_all("article")

            data = []
            translator = Translator()

            for article in articles:
                # Пример выбора заголовка и ссылки
                link = article.find("a")  # Возможно, вам потребуется изменить способ выбора
                href = link.get("href") if link else ""

                # Извлечение текста после последнего '/' и форматирование заголовка
                title = href.split("/")[5]
                title = title.replace("-", " ")

                # Перевод заголовка на русский
                translated_title = translator.translate(title, src='en', dest='ru').text

                data.append({"title": translated_title, "link": href})

            # Сохранение данных в JSON файл
            with open("coconut/coconuts.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print("Данные сохранены в coconuts_data.json.")
        else:
            print("Не удалось получить доступ к сайту. Код состояния:", response.status_code)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(fetch_data())
