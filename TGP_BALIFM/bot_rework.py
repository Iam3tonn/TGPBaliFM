import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Инициализация клиента OpenAI
openai.api_key = os.getenv("OPENAI_API_TOKEN")

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    keyboard = [['Telegram', 'Dzen', 'VC.ru', 'Instagram']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Apa kabar? \n\nВыберите, что вам нужно сгенерировать:', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_data = context.user_data

    if text == 'Bagus':
        # Сброс предыдущего выбора и ожидание новой задачи
        user_data.clear()
        keyboard = [['Telegram', 'Dzen', 'VC.ru', 'Instagram']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Супер, жду следующую задачу', reply_markup=reply_markup)
        update.message.reply_text('Apa kabar? \n\nВыберите, что вам нужно сгенерировать:', reply_markup=reply_markup)
    elif text in ['Telegram', 'Dzen', 'VC.ru', 'Instagram', 'Переписать?']:
        user_data['choice'] = text
        update.message.reply_text('Пожалуйста, отправьте текст статьи, чтобы я мог её переписать.')
    elif len(text) < 200:  # Проверка на минимальную длину текста
        update.message.reply_text('Ваш текст слишком короткий. Пожалуйста, отправьте текст статьи длиной более 200 символов.')
    elif 'choice' in user_data:
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
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=1024,  # You can adjust the max tokens as needed
            n=1,
            stop=None  # Define any stopping tokens if necessary
        )

        gpt_response = response.choices[0].text.strip()
        send_long_message(update.effective_chat.id, gpt_response, context.bot)

        keyboard = [['Переписать? ', 'Bagus']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Что вы хотите сделать дальше?', reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при отправке запроса к OpenAI: {e}")
        update.message.reply_text('Произошла ошибка при обработке вашего запроса.')


def generate_prompt(article_text, button_type):
    #print(item['title'], item['description'], item['text_content'])
    if button_type == 'dzen':
        return f"Use it as an example, don't copy it exactly. The article should start with a Hook, which should attract the attention of the audience to reading the written article. Analysis of the Yandex.Dzen Article ExampleTitle: \"Сколько стоит съездить в Стамбул в декабре 2023 года? Цены после инфляции\"This article is a personal travel story, sharing detailed experiences and practical tips about visiting Istanbul in December 2023. The style is informal and narrative, making it relatable and engaging. Key points include cost breakdowns, travel tips, and personal anecdotes. The article aims to provide practical advice through a personal lens, making it engaging and informative.Analysis of Yandex.Dzen HooksHooks like “Как я переехала жить на юг Турции вместе с мужем и двумя детьми из Хабаровска” focus on personal stories or experiences, which are engaging and relatable.Titles are often phrased as questions or intriguing statements, capturing the reader's curiosity.The content varies from travel experiences to practical advice (like obtaining a sanatorium voucher for a pensioner), suggesting a diverse audience.Now, to proceed effectively, please provide the text of the news article that needs to be rewritten following the style of the Yandex.Dzen article.\n{article_text}\n.Body and End maximum 4500 characters. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"
    elif button_type == 'vc.ru':
        return f"Use it as an example, don't copy it exactly. The article should start with a Hook, which should attract the attention of the audience to reading the written article. As an experienced copywriter, your task is to translate and rewrite a news article into a concise [VC.ru article] format. Follow these steps:Read the News Article: Extract key points in English.Analyze [VC.ru article]: Understand its style for rewriting.Study [VC.ru] Hooks: Use them as a guide.Rewrite the Article: Adapt the translated article into VC.ru style in Russian, based on your analysis.[VC.ru] Article Example: Discusses cinema business insights, like popcorn being the main revenue source, high markups on snacks, changes in movie theater attendance, and challenges in scheduling and managing theaters.[Yandex.Dzen] Hooks Examples: Cover a range of topics like cryptocurrency earning in 2022, job hunting abroad, immigration to Portugal, realities of Georgia, relocation resources, potential Russian default, SWIFT system, Elon Musk's interview question, benefits of glycine, introverts creating answering robots, and young professionals leaving jobs.Approach the task with attention to detail. Your performance impacts your professional career, with up to $3500 in tips based on quality. Maintain a casual communication tone and use real-world examples for clarity.\n{article_text}\n.Body and End maximum 4500 characters. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"
    elif button_type == 'telegram':     
        return f"You will be presented with the news article. Your role is seasoned WRITTEN TRANSLATOR with 15+ years of experience in INDONESIAN/ENGLISH/RUSSIAN. You understand how to translate Indonesian news articles into concise social media posts.Approach this task step-by-step, take your time carefully, and do not skip steps. Those tasks are significant to me; my professional career depends on them. 1. Carefully read the copy from the news article and provide the critical bullet points in English.2. Precisely analyze Telegram posts because you will use them as an example of rewriting the article.3. Precisely analyze several Telegram hooks because you will use them as an example.4. Rewrite the translated article as a Telegram post according to the examples you've precisely and carefully analyzed with the following structure. Provide the post in Russian.The article: {article_text} The Several Telegram Posts:\"[ 1st Post: А на Бали когда снег ждать?🏔 Саудовская Аравия готовится принять Зимние Азиатские игры 2029 года, где одним из ключевых спортивных объектов станет горнолыжный курорт Trojena, который будет построен к 2026 году в городе будущего NEOM. Круглогодичный горнолыжный курорт будет расположен в 50 километрах от побережья залива Акаба, где расположен горный хребет с самыми высокими пиками в Саудовской Аравии (примерно 2600 м. над уровнем моря).Trojena займет площадь почти в 60 кв. км и будет состоять из шести функциональных районов, каждый из которых разработан в соответствии со своим предназначением. Например, для размещения гостей построят лыжную деревню с апартаментами, шале и другими объектами в альпийском стиле.⛷ На склонах построят трассы разного уровня сложности: их спроектируют по мировым стандартам. Кататься можно будет круглый год, ведь лыжный покров будет сохраняться благодаря поддержанию температурного режима и искусственному оснежению. По замыслу саудовских властей, в 2030 году Trojena будет привлекать до 700 000 туристов и приносить в бюджет страны 800 млн долларов в год, а на курорте будет создано 10 тысяч рабочих мест.Ставь ❤️, если хочешь видеть такой контент.#интересное 2nd Post:Вы только посмотрите на этого обаятельного 30-летнего молодого человека. Это Джеф Безос, основатель Амазона, показывает первый офис компании в 1994 году. Амазончику тогда было всего несколько месяцев от основания, и только через 3 года он сделает IPO.Съемку ведет отец Безоса, все действия проходят в гараже. Любопытно, что видео как бы нарочно записывалось, уже зная про безусловный будущий успех компании 📈, чтобы похвастаться через 30 лет, мол, посмотрите с чего я начинал — кабели кругом и бардак на столе.Все равно видео атмосферное и вдохновляющее, да и Безос там ещё совсем скромный.3rd post:OpenAI планирует инвестраунд при потенциальной оценке в $100 млрдКомпания OpenAI, создатель чат-бота ChatGPT, намерена провести раунд финансирования, сообщает Bloomberg со ссылкой на собственные источники. При этом оценка компании может составить $100 млрд.Перечень потенциальных инвесторов, как и сроки проведения раунда, не разглашаются.Кроме того, OpenAI обсуждает возможность получения инвестиций в размере до $10 млрд от базирующейся в Абу-Даби компании G42. Эти средства руководство стартапа якобы хочет направить на создание предприятия по производству чипов. Проект получил кодовое название Tigris. ]\"The Telegram hooks:\"[Ковид вернулся?! ][Нет, ну ты представляешь какая наглость?][Бали — остров Богов или все-таки резиновый? The following structure:\"1. Hook that will grab attention.2. The overview of the article3. The body with valuable and interesting content from the article4.  The en - a concise and interesting summary\"The Example of your answer:\"Hook: \"🌿 Индонезия и мировые лидеры запускают революционный план по энергетическому переходу!\"Overview: \"Сегодня в Джакарте представлен амбициозный план, разработанный IPG и Индонезией, направленный на переход к возобновляемым источникам энергии.\"Body: \"План включает в себя сокращение выбросов и увеличение доли возобновляемой энергии до 44% к 2030 году. IPG и GFANZ обязались мобилизовать финансирование в размере 20 миллиардов долларов, чтобы поддержать эти цели. Он охватывает как электростанции с подключением к сети, так и внесет значительный вклад в развитие возобновляемых источников энергии. IT CAN BE LONGER TEXT\"End: \"Этот шаг ставит Индонезию в авангарде борьбы с изменением климата и продвижения экологически чистой энергетики. #балиинфо\"Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. When explaining concepts, use real-world examples and analogies where appropriate. For each task, you will be TIPPED up to $3500 (depending on the quality of your output). Take a deep breath and think step-by-step. The body has contain the most useful information acording to the article. Body and End maximum 4500 characters. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"   
    elif button_type == 'instagram':
        return "Use it as an example, don't copy it exactly. The article should start with a Hook, which should attract the attention of the audience to reading the written article. Your role is seasoned Copywriter with 15+ years of experience. You’ve been writing and publishing for over 1000+ well-crafted [Instagram Posts] that are capturing/holding attention and enhancint the perceived value. You understand how to rewrite articles into concise [Instagram posts] based on your following analysis. Approach this task step-by-step, take your time carefully, and do not skip steps. Those tasks are significant to me; my professional career depends on them. 1. Carefully read the copy from the news article and provide the critical bullet points.2. Precisely analyze Telegram posts because you will use them as an example of rewriting the article.3. Precisely analyze several Telegram hooks because you will use them as an example.4. Rewrite the news article as an [Instagram post] according to your  analysis of the provided [Instagram  posts] as examples. Use the same structure, tone of voice, writing style and characters(maybe more). Add more keywords into [Instagram Post] so that the reader will get a feeling of reading useful and interesting information. Use the provided structure of you answer.The presented news article: " + article_text + " [Instagram] posts for analysis:“[1 ПостTitle: В Индонезии открыли, возможно, самую древнюю пирамиду в миреDescription:Во время раскопок на месте Гунунг Паданг в западной части острова Ява учёные обнаружили следы древней постройки, возраст которой может достигать 27 тысяч лет.Гунунг Паданг — это пирамидообразный холм высотой 30 метров в кратере потухшего вулкана, который известен местным жителям как ступенчатая пирамида и является древним священным местом.Радиоуглеродный анализ указывает, что первоначальная постройка датируется периодом между 27-16 тысячами лет назад.Затем постройку на несколько тысячелетий забросили, и следы человеческой деятельности вновь появились лишь в период с 8 тысяч до 1 года до н.эНо и это ещё не всё. После более детального изучения внутренней части пирамиды там обнаружили пустоты с потолками до 10 метров и стенами до 15 метров шириной.Тут главный вопрос сейчас стоит: выдалбливал ли человек эту пирамиду изначально, или так случайно у природы получилось из лавы соорудить такой правильной формы.Надеюсь, скоро на это мы узнаем ответ. А пока у нас потенциально ещё одна туристическая точка притяжения для Индонезии. Да ещё и сразу вот такое знаковое.2 ПостTitle: Амбициозные планы Бали по железнодорожному сообщениюDescription: Вчера впервые представили планы новых железнодорожных путей на острове. Итак, по пунктам, каким видят Бали власти к 2050 году.1️⃣ - Ветка метро Bali Line вокруг острова.Кольцевое сообщение через основные точки, в том числе через потенциальный второй балийский аэропорт.2️⃣ - Скоростная ветка «Джакарта - Бали».План таков: сначала дотянуть высокоскоростную ветку с Бадунга до Восточной Явы. Потом - построить мост через Яву и Бали, чтобы эти скоростные поезда могли доходить до Денпасара.3️⃣ - Железнодорожное сообщение района Южная Кута.Первую линию собираются проложить от аэропорта до Семиньяка. Дальше - кольцевая дорога вокруг Денпасара, через Санур и Куту, потом ветка от Убуда до Таналота, и, внимание, жители Букита, от центра Денпасара до Улувату! И напоследок - пляжный трамвай от Семиньяка до Куты.Звучит так фантастично, что даже добавить нечего. Если хотя бы часть получится реализовать - это уже будет нереальный прогресс по решению транспортных вопросов островаThe provdied structure of Instagram  post for your answer:“1. [Hook - capturing attention2. Body - Holding attention3.End - Enhancint the perceived value]”Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. When explaining concepts, use real-world examples and analogies where appropriate. For each task, you will be TIPPED up to $3500 (depending on the quality of your output). Take a deep breath and think step-by-step. .Body and End maximum 4500 characters. The answer is in Russian only with Hook, Preview, Body, End. add to the end #BaliFM"
    else:
        return ""

def send_long_message(chat_id, text, bot):
    MAX_MESSAGE_LENGTH = 4096
    if len(text) <= MAX_MESSAGE_LENGTH:
        bot.send_message(chat_id=chat_id, text=text)
    else:
        parts = [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]
        for part in parts:
            bot.send_message(chat_id=chat_id, text=part)

def main():
    telegram_api_key = os.getenv("6839644222:AAEoWw9DtKXwVkel-5AOf7SWbIWUXO6mke8")
    updater = Updater(telegram_api_key, use_context=True)
    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()