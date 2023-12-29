# 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
# 6839644222:AAEoWw9DtKXwVkel-5AOf7SWbIWUXO6mke8
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен API ChatGPT должен быть защищен. Не храните его в коде. Лучше использовать переменные окружения или зашифрованный файл конфигурации.
CHATGPT_API_TOKEN = "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"

def start(update: Update, context: CallbackContext):
    keyboard = [['Telegram', 'Dzen', 'VC.ru']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Apa kabar? \n\nВыберите, что вам нужно сгенерировать:', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_data = context.user_data

    if text == 'Bagus':
        # Сброс предыдущего выбора и ожидание новой задачи
        user_data.clear()
        keyboard = [['Telegram', 'Dzen', 'VC.ru']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text('Супер, жду следующую задачу', reply_markup=reply_markup)
        update.message.reply_text('Apa kabar? \n\nВыберите, что вам нужно сгенерировать:', reply_markup=reply_markup)
    elif text in ['Telegram', 'Dzen', 'VC.ru']:
        user_data['choice'] = text
        update.message.reply_text('Пожалуйста, отправьте текст статьи, чтобы я мог её переписать.')
    elif 'choice' in user_data:
        if len(text) < 200:  # Проверка на минимальную длину текста
            update.message.reply_text('Ваш текст слишком короткий. Пожалуйста, отправьте текст статьи длиной более 200 символов.')
        else:
            user_data['article_text'] = text
            update.message.reply_text('Ожидайте, идет обработка запроса...')
            send_to_chatgpt(update, context)
    else:
        update.message.reply_text('Выберите опцию из меню.')


def send_to_chatgpt(update: Update, context: CallbackContext):
    user_data = context.user_data
    article_text = user_data.get('article_text')
    choice = user_data.get('choice')

    if not article_text or not choice:
        update.message.reply_text('Произошла ошибка. Пожалуйста, начните заново.')
        return

    prompt = generate_prompt(article_text, choice.lower())

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers={"Authorization": f"Bearer {CHATGPT_API_TOKEN}"},
                                 json={
                                     "model": "gpt-3.5-turbo",
                                     "messages": [{"role": "system", "content": "You are a helpful assistant."},
                                                  {"role": "user", "content": prompt}]
                                 })

        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            context.bot.send_message(chat_id=update.effective_chat.id, text=gpt_response)
            keyboard = [['Переписать? ', 'Bagus']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text('Что вы хотите сделать дальше?', reply_markup=reply_markup)
        else:
            error_message = f"Ошибка: {response.status_code} - {response.text}"
            update.message.reply_text(error_message)
    except Exception as e:
        logger.error(f"Ошибка при отправке запроса к ChatGPT: {e}")
        update.message.reply_text('Произошла ошибка при обработке вашего запроса.')


def generate_prompt(article_text, button_type):
    #print(item['title'], item['description'], item['text_content'])
    if button_type == 'dzen':
        return f"You will be presented with the information that I want you to rewrite as [AN ARTICLE FOR Yandex.Dzen]. Your role is seasoned Copywriter with 15+ years of experience in [INDONESIAN/ENGLISH/RUSSIAN] languages. You’ve been writing and publishing 1000+ well-crafted articles that resonate with people's interests about [life as an expat in Bali, Indonesia]. You understand how to rewrite the provided information concisely [Yandex.Dzen].Approach this task step-by-step, take your time carefully, and DO NOT SKIP STEPS. Those tasks are significant to me; my professional career and life depend on them. 1. Carefully read the copy of the information that I want to rewrite and provide the critical bullet points in English.2. Precisely and carefully analyze ALL [articles from Yandex.Dzen] in the WORD file. You will use them as an example of rewriting the information.3. Precisely and carefully analyze ALL [Yandex.Dzen article’s hooks]. You will use them as an example.4. Rewrite the translated article as a [Yandex.Dzen article] according to the examples you've precisely and carefully analyzed in the attached WORD file. Provide a concise article for Yandex.Dzen about according to the provided information that I want to rewrite in the Russian language. The information that I want to rewrite: {article_text} .The Yandex.Dzen hooks: “[Сколько стоит съездить в Стамбул в декабре 2023 года? Цены после инфляцииКак я переехала жить на юг Турции вместе с мужем и двумя детьми из Хабаровска. Рассказываю личный опыт4 места в России, где тепло поздней осеньюКак пенсионеру получить путёвку в санаторий8 стран, в которые можно полететь зимой без визы]”Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. When explaining concepts, use real-world examples and analogies where appropriate. For each task, you will be TIPPED up to $3500 (depending on the quality of your output). Take a deep breath and think step-by-step.  The body has contain the most useful information acording to the article. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"    
    elif button_type == 'vc.ru':
        return f"You will be presented with the information that I want you to rewrite as [AN ARTICLE FOR VC.ru]. Your role is seasoned Copywriter with 15+ years of experience in [INDONESIAN/ENGLISH/RUSSIAN] languages. You’ve been writing and publishing 1000+ well-crafted articles that resonate with people's interests about [life as an expat in Bali, Indonesia]. You understand how to rewrite the provided information concisely [VC.ru article].Approach this task step-by-step, take your time carefully, and DO NOT SKIP STEPS. Those tasks are significant to me; my professional career and life depend on them. 1. Carefully read the copy from the news article and provide the critical bullet points in English.2. Precisely and carefully analyze ALL [articles from VC.ru] in the WORD file. You will use them as an example of rewriting the article.3. Precisely and carefully analyze ALL [VC.ru article’s hooks]. You will use them as an example.4. Rewrite the translated article as an [VC.ru article] according to the examples you've precisely and carefully analyzed in the attached WORD file. Provide a concise article for VC.ru according to the information I want to rewrite in Russian. The information that I want to rewrite: {article_text}. The hooks from articles from VC.ru: “[Как зарабатывать на криптовалюте в 2022 году, если ты — нулевой Как найти работу за границей: большая подборка каналов, чатов и сервисов Иммиграция в Португалию по D7 визе (пассивный доход). Мой опыт получения визы и план на ВНЖ Реальная Грузия: грустные факты, которые вас разочаруют Подборка ресурсов для релокации и эмиграции Россию ждет дефолт? Что делать? Что такое SWIFT и что будет, если Россию от него отключат: коротко101 способ упростить себе жизнь: маленькие приёмы, которые решают большие проблемыКупленные вами акции вам никогда не принадлежали и не будут принадлежатьУчёные подтвердили эффективность главного вопроса Илона Маска на собеседованиях«Таблетка для ума»: зачем принимают глицин и может ли он помочь организму на самом делеЯ интроверт — не люблю разговаривать по телефону. Поэтому я создал робота Машу — теперь она отвечает на все звонки Канарейку за копейку — почему молодые спецы от вас сбегаютМаленькие секреты работы кинотеатров. Рассказываю, как они работают]”Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. When explaining concepts, use real-world examples and analogies where appropriate. For each task, you will be TIPPED up to $3500 (depending on the quality of your output). Take a deep breath and think step-by-step.  The body has contain the most useful information acording to the article. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"   
    elif button_type == 'telegram':
        return f"You will be presented with the news article. Your role is seasoned WRITTEN TRANSLATOR with 15+ years of experience in INDONESIAN/ENGLISH/RUSSIAN. You understand how to translate Indonesian news articles into concise social media posts.Approach this task step-by-step, take your time carefully, and do not skip steps. Those tasks are significant to me; my professional career depends on them. 1. Carefully read the copy from the news article and provide the critical bullet points in English.2. Precisely analyze Telegram posts because you will use them as an example of rewriting the article.3. Precisely analyze several Telegram hooks because you will use them as an example.4. Rewrite the translated article as a Telegram post according to the examples you've precisely and carefully analyzed with the following structure. Provide the post in Russian.The article: {article_text} The Several Telegram Posts:\"[ 1st Post: А на Бали когда снег ждать?🏔 Саудовская Аравия готовится принять Зимние Азиатские игры 2029 года, где одним из ключевых спортивных объектов станет горнолыжный курорт Trojena, который будет построен к 2026 году в городе будущего NEOM. Круглогодичный горнолыжный курорт будет расположен в 50 километрах от побережья залива Акаба, где расположен горный хребет с самыми высокими пиками в Саудовской Аравии (примерно 2600 м. над уровнем моря).Trojena займет площадь почти в 60 кв. км и будет состоять из шести функциональных районов, каждый из которых разработан в соответствии со своим предназначением. Например, для размещения гостей построят лыжную деревню с апартаментами, шале и другими объектами в альпийском стиле.⛷ На склонах построят трассы разного уровня сложности: их спроектируют по мировым стандартам. Кататься можно будет круглый год, ведь лыжный покров будет сохраняться благодаря поддержанию температурного режима и искусственному оснежению. По замыслу саудовских властей, в 2030 году Trojena будет привлекать до 700 000 туристов и приносить в бюджет страны 800 млн долларов в год, а на курорте будет создано 10 тысяч рабочих мест.Ставь ❤️, если хочешь видеть такой контент.#интересное 2nd Post:Вы только посмотрите на этого обаятельного 30-летнего молодого человека. Это Джеф Безос, основатель Амазона, показывает первый офис компании в 1994 году. Амазончику тогда было всего несколько месяцев от основания, и только через 3 года он сделает IPO.Съемку ведет отец Безоса, все действия проходят в гараже. Любопытно, что видео как бы нарочно записывалось, уже зная про безусловный будущий успех компании 📈, чтобы похвастаться через 30 лет, мол, посмотрите с чего я начинал — кабели кругом и бардак на столе.Все равно видео атмосферное и вдохновляющее, да и Безос там ещё совсем скромный.3rd post:OpenAI планирует инвестраунд при потенциальной оценке в $100 млрдКомпания OpenAI, создатель чат-бота ChatGPT, намерена провести раунд финансирования, сообщает Bloomberg со ссылкой на собственные источники. При этом оценка компании может составить $100 млрд.Перечень потенциальных инвесторов, как и сроки проведения раунда, не разглашаются.Кроме того, OpenAI обсуждает возможность получения инвестиций в размере до $10 млрд от базирующейся в Абу-Даби компании G42. Эти средства руководство стартапа якобы хочет направить на создание предприятия по производству чипов. Проект получил кодовое название Tigris. ]\"The Telegram hooks:\"[Ковид вернулся?! ][Нет, ну ты представляешь какая наглость?][Бали — остров Богов или все-таки резиновый? The following structure:\"1. Hook that will grab attention.2. The overview of the article3. The body with valuable and interesting content from the article4.  The en - a concise and interesting summary\"The Example of your answer:\"Hook: \"🌿 Индонезия и мировые лидеры запускают революционный план по энергетическому переходу!\"Overview: \"Сегодня в Джакарте представлен амбициозный план, разработанный IPG и Индонезией, направленный на переход к возобновляемым источникам энергии.\"Body: \"План включает в себя сокращение выбросов и увеличение доли возобновляемой энергии до 44% к 2030 году. IPG и GFANZ обязались мобилизовать финансирование в размере 20 миллиардов долларов, чтобы поддержать эти цели. Он охватывает как электростанции с подключением к сети, так и внесет значительный вклад в развитие возобновляемых источников энергии. IT CAN BE LONGER TEXT\"End: \"Этот шаг ставит Индонезию в авангарде борьбы с изменением климата и продвижения экологически чистой энергетики. #балиинфо\"Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. When explaining concepts, use real-world examples and analogies where appropriate. For each task, you will be TIPPED up to $3500 (depending on the quality of your output). Take a deep breath and think step-by-step. The body has contain the most useful information acording to the article. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"   
    else:
        return ""

def main():
    updater = Updater("6839644222:AAEoWw9DtKXwVkel-5AOf7SWbIWUXO6mke8", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

