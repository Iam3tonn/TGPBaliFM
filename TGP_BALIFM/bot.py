import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from urllib.parse import urlparse

# Устанавливаем токен вашего бота и URL для ChatGPT
TOKEN = '6839644222:AAEoWw9DtKXwVkel-5AOf7SWbIWUXO6mke8'
#GPT_API_URL = 'https://api.openai.com/v1/chat/completions'  # Замените на актуальный URL для ChatGPT
#GPT_API_KEY = 'YOUR_CHATGPT_API_KEY'

# Инициализируем сессию requests
session = requests.Session()

#session.headers.update({
#    'Authorization': f'Bearer {GPT_API_KEY}',
#    'Content-Type': 'application/json',
#})


# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Определение состояний бота
START, CHOOSE_PLATFORM, PROMPT_GENERATION, REGENERATE_PROMPT, WAITING_FOR_LINK = range(5)

# Словарь для хранения ссылок пользователей
user_links = {}


# Обработка команды /start
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.user_data['state'] = START
    update.message.reply_text(f"Привет, {user.first_name}! Я бот, который генерирует текст на основе ваших ссылок.")
    return ask_for_link(update, context)


# Обработка команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Этот бот генерирует текст на основе предоставленных вами ссылок. "
                              "Просто отправьте мне ссылку, и я предложу вам две опции для генерации текста.")


# Функция, запрашивающая у пользователя ссылку
def ask_for_link(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Пожалуйста, отправьте мне ссылку на сайт.")
    context.user_data['state'] = WAITING_FOR_LINK
    return WAITING_FOR_LINK


# Функция, обрабатывающая полученную ссылку
def handle_link(update: Update, context: CallbackContext) -> int:
    # Predefined list of links
    allowed_links = ['https://www.detik.com/bali']

    user = update.message.from_user
    url = update.message.text
    parsed_url = urlparse(url)

    print(parsed_url)

    if parsed_url.scheme and parsed_url.netloc:
        if url in allowed_links:
            user_links[user.id] = url
            context.user_data['state'] = CHOOSE_PLATFORM
            keyboard = [['Яндекс Дзен', 'VC.ru']]
            markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text("Выберите платформу для генерации текста:", reply_markup=markup)
            return CHOOSE_PLATFORM
        else:
            update.message.reply_text("Данная ссылка не разрешена. Пожалуйста, используйте другую.")
            return ask_for_link(update, context)
    else:
        update.message.reply_text("Вы ввели некорректную ссылку. Пожалуйста, попробуйте еще раз.")
        return ask_for_link(update, context)


# Функция, обрабатывающая выбор платформы для генерации текста
def choose_platform(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    platform = update.message.text.lower()
    context.user_data['platform'] = platform
    context.user_data['state'] = PROMPT_GENERATION
    
    # Получаем сохраненную ссылку для данного пользователя
    user_link = user_links.get(user.id, "Ссылка не найдена")
    
    prompt = f"Генерация текста для ссылки: {user_link}, на платформе: {platform}"
    generated_text = generate_text_with_chatgpt(prompt)
    update.message.reply_text(generated_text)
    keyboard = [['Переделать', 'Прислать новую ссылку']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Что вы хотите сделать дальше?", reply_markup=markup)
    return REGENERATE_PROMPT


# Функция, обрабатывающая запрос на перегенерацию текста
def regenerate_prompt(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'переделать':
        context.user_data['state'] = PROMPT_GENERATION
        user = update.message.from_user
        platform = context.user_data['platform']
        prompt = f"Генерация текста для ссылки: {user_links[user.id]}, на платформе: {platform}"
        generated_text = generate_text_with_chatgpt(prompt)
        update.message.reply_text(generated_text)
        keyboard = [['Переделать', 'Прислать новую ссылку']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text("Что вы хотите сделать дальше?", reply_markup=markup)
        return REGENERATE_PROMPT
    elif choice == 'прислать новую ссылку':
        return ask_for_link(update, context)
    else:
        update.message.reply_text("Пожалуйста, воспользуйтесь кнопками.")
        return REGENERATE_PROMPT


# Функция для отправки запроса к API ChatGPT
def generate_text_with_chatgpt(prompt: str) -> str:
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': prompt}]
    }

    response = session.post(GPT_API_URL, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Произошла ошибка при запросе к ChatGPT API. Код ошибки: {response.status_code}"


# Функция, обрабатывающая неизвестные команды
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Извините, я не понимаю эту команду.")


def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))
    dp.add_handler(MessageHandler(Filters.regex('^(Яндекс Дзен|VC.ru)$'), choose_platform))
    dp.add_handler(MessageHandler(Filters.regex('^(Переделать|Прислать новую ссылку)$'), regenerate_prompt))
    dp.add_handler(MessageHandler(Filters.text, unknown))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
