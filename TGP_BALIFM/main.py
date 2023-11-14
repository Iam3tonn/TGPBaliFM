import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import schedule
import subprocess
import random 
 

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
bot = Bot(token='6524320610:AAHgv6pft_059D996yAVKr9zEqQUj7iSPmk')
dp = Dispatcher(bot)

# Замените 'CHANNEL_ID' на ID вашего канала
channel_id = -1002121080519  # Уберите знак "-" перед ID, если у вас приватный канал

# Множество для хранения уже отправленных ссылок
sent_links = set()

family_friendly = [
                   "погибли", "погаорели", "арест", "суд", "тюрьму", "тюрьма", "гениталии", "гениталия", "половой", "интимный", "интинмая", "половым",
                   "криминал", "преступность", "убийство", "преступность", "преступная", "мертвый", "мертвыми", "эрекции", "пенис", "насилии", "насилие",
                   "бомбардировщик", "приступности", "наркотики", "наркотиках", "наркотикам", "погибли", "погибла", "погиб", "мертвая", "мертвым", "незаконной",
                   "госпитализирована","госпитализированы", "госпитализирован", "изнасиловали", "изнасиловал", "казахстанском"
                   ]

# Функция для отправки новых данных в канал
async def send_new_data():
    with open('combined_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        random.shuffle(data)

        for item in data:
            title = item['title']
            link = item['link']

            # Check if any word in the title is in the family_friendly list
            if all(word.lower() in title.lower() for word in family_friendly):
                print(f"Пропуск новости с названием: {title}")
                continue

            # Check if the link has already been sent
            if link not in sent_links:
                message = f"{title}\n\n{link}"
                await bot.send_message(chat_id=channel_id, text=message)
                sent_links.add(link)
                # Перерыв между отправками записей в телеграм 20 секунд
                await asyncio.sleep(20)

# Функция для выполнения jsons_files.py


def execute_jsons_files():
    import jsons_files
    print("Начало jsons_files")
    print(" ")
    jsons_files.main()  # предполагая, что у вас есть функция main в файле jsons_files.py

if __name__ == "__execute_jsons_files__":
    execute_jsons_files()
    

# Главная функция
async def main():
    while True:
        # Сначала выполнить jsons_files.py
        execute_jsons_files()

        # Затем отправить новые данные
        #await send_new_data()

        await asyncio.sleep(1800)  # Ожидание 30 минут (1800 секунд)

if __name__ == '__main__':
    # Планирование выполнения jsons_files.py каждые 10 минут
    schedule.every(20).minutes.do(execute_jsons_files)

    loop = asyncio.get_event_loop()
    loop.create_task(main())

    # Запуск планировщика schedule
    while True:
        schedule.run_pending()
        loop.run_until_complete(asyncio.sleep(1))