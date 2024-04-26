import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import schedule
import subprocess
import random 
 
# Импортируем необходимые библиотеки. 
# asyncio - для асинхронного программирования, aiogram - для работы с Telegram Bot API,
# schedule - для планирования задач, random - для случайного выбора элементов.

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
bot = Bot(token='7190426477:AAHaNQgUV4cFZzxTpl62Aajboigr9Y04LXI')
dp = Dispatcher(bot)

# Замените 'CHANNEL_ID' на ID вашего канала
channel_id = -1002057745919  # Уберите знак "-" перед ID, если у вас приватный канал

# Множество для хранения уже отправленных ссылок
sent_links = set()

family_friendly = [
                   "погибли", "погаорели", "арест", "суд", "тюрьму", "тюрьма", "гениталии", "гениталия", "половой", "интимный", "интинмая", "половым",
                   "криминал", "преступность", "убийство", "преступность", "преступная", "мертвый", "мертвыми", "эрекции", "пенис", "насилии", "насилие",
                   "бомбардировщик", "приступности", "наркотики", "наркотиках", "наркотикам", "погибли", "погибла", "погиб", "мертвая", "мертвым", "незаконной",
                   "госпитализирована","госпитализированы", "госпитализирован", "изнасиловали", "изнасиловал", "казахстанском"
                   ]

async def send_new_data():
    # Асинхронная функция для отправки данных в Telegram канал.
    try:
        with open('combined_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            random.shuffle(data)  # Перемешиваем данные для случайного выбора.

            for item in data:
                # Проходим по каждому элементу в данных.
                title = item['title']
                link = item['link']
                date = item['date']

                # Проверяем, не содержит ли заголовок запрещенные слова.
                if any(word.lower() in title.lower() for word in family_friendly):
                    print(f"Skipping news with title: {title}")
                    continue

                if link not in sent_links:
                    # Если ссылка еще не отправлялась, отправляем ее.
                    message = f"{title}\n\n{link}\n\n<i>{date}</i>"
                    await bot.send_message(chat_id=channel_id, text=message, parse_mode='HTML')
                    sent_links.add(link)  # Добавляем ссылку в множество отправленных.
                    await asyncio.sleep(20)  # Задержка между отправками сообщений.
    except Exception as e:
        print(f"Error in send_new_data: {e}")

def execute_jsons_files():
    # Функция для выполнения скрипта jsons_files.py.
    try:
        import jsons_files
        print("Starting jsons_files")
        jsons_files.main()  # Вызов функции main из jsons_files.py.
    except Exception as e:
        print(f"Error in execute_jsons_files: {e}")
        # Обработка ошибок.

if __name__ == "__execute_jsons_files__":
    execute_jsons_files()

# Главная функция
async def main():
    while True:
        try:
            # Сначала выполнить jsons_files.py
            execute_jsons_files()

            # Затем отправить новые данные
            await send_new_data()

            await asyncio.sleep(1800)  # Ожидание 30 минут (1800 секунд)
        except Exception as e:
            print(f"Произошла ошибка в main: {e}")

if __name__ == '__main__':
    # Планирование выполнения jsons_files.py каждые 10 минут
    schedule.every(20).minutes.do(execute_jsons_files)

    loop = asyncio.get_event_loop()
    loop.create_task(main())

    # Запуск планировщика schedule
    while True:
        schedule.run_pending()
        loop.run_until_complete(asyncio.sleep(1))