import logging
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os


# Инициализация клиента OpenAI
#openai.api_key = "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"
openai.api_key = os.getenv('OPENAI_API_KEY')

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
    elif text == 'Переписать?':
        # Если пользователь нажимает "Переписать?", возвращаем его к выбору типа сайта
        user_data.clear()
        keyboard = [['Telegram', 'Dzen', 'VC.ru', 'Instagram']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Выберите, что вам нужно сгенерировать:', reply_markup=reply_markup)
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
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        gpt_response = response['choices'][0]['message']['content']
        send_long_message(update.effective_chat.id, gpt_response, context.bot)

        keyboard = [['Переписать? ', 'Bagus']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Что вы хотите сделать дальше?', reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при отправке запроса к OpenAI: {e}")
        update.message.reply_text('Произошла ошибка при обработке вашего запроса.')



def generate_prompt(article_text, button_type):
    #print(item['title'], item['description'], item['text_content'])
    if button_type == 'dzen' or button_type == 'vc.ru':
        return f"Your role is seasoned Copywriter with 15+ years of experience. You’ve been writing and publishing over 1000+ well-crafted [News Articles] that are capturing/holding attention and enhancing the perceived value for the audience. Based on your following analysis, you understand how to rewrite information into an interesting and insightful [article]. Approach this task step-by-step, take your time carefully, and do not skip steps. Those tasks are significant to me; my professional career depends on them. 1. Carefully read the copy from the news article and provide all critical bullet points.2. Precisely analyze VC.ru articles because you will use them as an example of rewriting them into a VC.ru article.4. Rewrite the news article using your analysis of the provided [VC.ru] article examples. Provide your article in Russian.  Include more detailed information and interesting facts from the sample in the post. The article should be interesting and engaging for the readers, you are responsible for keeping the retention rate of followers as high as possible. Do NOT use emojis. Remember that the target language is Russian, so the post should be written according to the Russian grammar and punctuation rules, but in a casual tone. The article has to contain 7000 characters. The presented news article: {article_text}. The [VC.ru] article for analysis:'[Дорожает даже краска на коробки для пиццы: что последствия «спецоперации» сделали с фастфудом, ресторанами и кофейнями Придётся снова думать, какие продукты можно заменить местными (в этот раз будет сложнее). А что будет через месяц — совсем непонятно.Ресторан «Рыба на даче»Российский рынок общепита тоже переживает кризис из-за «спецоперации» в Украине. Из-за санкций прямые поставки одних товаров подорожали в разы, а других — стали почти невозможны.Рестораторы рассчитывают, что поставщики будут ввозить продукты в Россию через страны-посредники, ищут аналоги импортных товаров у отечественных производителей и собираются сами локализовать производство нужных ингредиентов.Кризис будет тяжелее, чем в 2014 году: оборот некоторых ресторанов за первую неделю санкций упал на 50%, говорят предприниматели. Но закрывать заведения владельцы пока не планируют и стараются решать проблемы по мере их поступления.Импортные продукты дорожают каждый деньДоля импорта продовольствия в России остаётся существенной. Например, страна импортирует более 90% семян сахарной свёклы, почти 60% семян кукурузы и около 70% подсолнечника.Из-за кризиса и роста курса доллара цены на импортные овощи выросли на 40–50%. Особенно взлетел в цене зелёный болгарский перец — из-за ограничений на поставки из Турции и Ирана на рынке возник дефицит, рассказал директор по закупкам и логистике «Додо Пиццы» Владислав Мандрыка.В ближайшее время сеть уберёт из меню картофельные оладушки, которые заказывала в Польше. При этом картофель-фри останется — его пиццериям поставляет агрохолдинг «Белая Дача».Компания «Сибаристика», которая обжаривает кофе, поставляет его более чем 300 компаниям (в том числе «ВкусВиллу» и «Самокату») и управляет одноимёнными кофейнями, тоже получила новые цены от поставщиков.Стоимость импортной кинзы, перца, кабачков, салата айсберг, ягод, сахара, альтернативного молока и других товаров поднялась в среднем на 20–30%, рассказал основатель компании Илья Сорокин.В наших заведениях паназиатская кухня и роллы, поэтому мы работаем с азиатскими поставщиками: они объявили, что будут формировать цены на момент заказа и перешли на предоплату.Сайт, на котором мы заказываем хозтовары, висит, и пока заказы принимаются только по телефону. Цены на все продукты и расходники меняются каждый день, и окончательный прайс многие поставщики не дают нам до сих пор.Илья Сорокин, основатель «Сибаристики»Probka, «Рыба на даче», Mama Tuta и другие заведения ресторатора Арама Мнацаканова не импортируют продукты из-за рубежа напрямую, а закупают у дистрибьюторов с наценкой — даже вина собственных торговых марок. Многие продукты уже подорожали на 20–50%, говорит генеральный управляющий ресторанной группы Александр Батушанский.Сейчас компания ведёт переговоры с поставщиками, ищет альтернативу этих ингредиентов и готовится пересмотреть ассортимент блюд с импортными компонентами в составе.Поставщики сети ресторанов «Тануки» и холдинга Bulldozer Group, куда входят Eshak, Benvenuto и Manana, вели себя по-разному. Одни остановили поставки с 24 февраля до 9 марта, вторые отгрузили товары по старым ценам, а третьи — повысили цены на 40%, рассказал президент холдинга Александр Орлов.За последние две недели резко выросли в цене морепродукты: креветки, морские ежи, осьминог, чёрная икра и крабовое мясо. Трюфели и овощи тоже очень подорожали.Цены на алкоголь выросли примерно на 35–40%. Один из наших поставщиков вина отказался от сотрудничества с Россией, и другие виноделы тоже могут последовать его примеру.Александр Орлов, президент Bulldozer Group и сооснователь «Тануки»По данным Минсельхоза, российские производители полностью обеспечивают население мясом. Однако корма для скота импортные и будут дорожать, отмечает Дмитрий Левицкий, основатель попавшего в гид Michelin ресторана Riesling Boyz, компании для управления ресторанами Hurma Group и гастрономического фестиваля Gastreet в Сочи.Сейчас перед рестораторами стоят проблемы двух уровней: первый — глобальный, он относится к уровню экономики в целом. Если российские банки смогут выстоять санкционное давление без существенных сбоев, мы перейдём к решению проблем второго уровня — перестройке логистических цепочек.У отрасли уже есть опыт в импортозамещении с 2014 года, когда итальянский сыр нам поставляет Беларусь. Сейчас наши поставщики заняты переговорами о ввозе продуктов в Россию через-страны посредники. С Россией по-прежнему сотрудничают Турция, Египет и Казахстан, поэтому можно организовать поставки через них.Пока все рестораторы живут в режиме планирования одного дня: нашёл какие-то альтернативные продукты, изменил меню, договорился о новых ценах с поставщиками.Дмитрий Левицкий, основатель Hurma GroupЧто поменяют рестораторыВ «Додо» доля импортных ингредиентов 5%, рассказал Владислав Мандрыка. Важнейший из них — пицца-соус, который сети в основном поставляет итальянская компания Mutti. «Додо» планирует самостоятельно готовить соус из отечественных ингредиентов: и уже создала предодобренные образцы.Упаковку для пицц и одноразовую посуду сеть производит самостоятельно, но использует импортные типографские краски. Если возникнут перебои в поставках пигментов, компания готова отказаться от брендирования упаковок.В целом мы обеспечены запасами ингредиентов на два-три месяца. Поставщиков, которые полностью остановили отгрузки, пока нет. При этом производители, к примеру, кофе и моцареллы сталкиваются со сложностями при морских перевозках. Изменяются логистических цепочки, из морских в мультимодальные.Скорее всего, в течение одной-двух недель сформируются новые «правила игры» и появится большая определенность с цепочками поставок.Владислав Мандрыка, директор «Додо Пицца» по закупкам и логистике«Сибаристика» успела закупить кофе для своих заведений на три-пять месяцев вперёд. Зерно для обжарки на продажу теперь придётся оплачивать по курсу Центробанка на день вывоза товара со склада, рассказал Илья Сорокин. Это связано с перебоями при контейнерных перевозках, объясняет предприниматель.Большинство трейдеров зелёного кофейного зерна, которые покупают его за рубежом и продают российским обжарщикам в валюте, уже подняли цены на 25–30% плюс курс доллара вырос с 75 до 121 рубля. Причём большинство трейдеров продают зерно не по курсу Центробанка, а по курсу покупки валюты, а это — 140 рублей за $1.Подорожание кофе связано с тем, что крупнейшие контейнерные грузоперевозчики остановили поставки в Россию. По информации Санкт-Петербургского порта, 85% поставок в город остановились.Российские импортёры зелёного зерна говорят, что у них есть проблемы с вывозом контейнеров из Роттердама. Мы не отчаиваемся и надеемся, что кофе будут возить китайские грузоперевозчики. Но уже сейчас наблюдаем, что чашка кофе в заведениях подорожала на 30–70 рублей.Илья Сорокин, основатель «Сибаристики»Запасов пакетов для кофе «Сибаристике» хватит на полгода, после чего компания планирует перейти на упаковку отечественного производства. Сорокин отказался от хозтоваров шведской фирмы Tork в пользу местных производителей.Почему российские продукты не будут дешевле импортныхАлександр Батушанский, генеральный управляющий ресторанов Арама Мнацаканова, не верит в полное импортозамещение. По его словам, с момента первых санкций зарубежных стран против России в 2014 году наши продукты даже не приблизились по качеству к импортным.К сожалению, у российских производителей нет аналогов многим ингредиентам — взять хоть тот же пресловутый пармезан. Чтобы сделать сыр европейского качества, помимо знаний и опыта требуется организовать длительный производственный цикл.Для этого нужны дешёвые кредиты и значительные оборотные средства. У сельского хозяйства в России их как не было, так и нет до сих пор. А в нынешних условиях о таком производстве даже бессмысленно и говорить.Мы до сих пор не решили проблемы 2014 года: ничего хорошего для бизнеса в санкциях не было, и у нас в стране так и не научились массово производить качественные продукты.А те, что научились, в условиях фактически монопольного положения, — постоянно повышали цены. Яркий пример — рынок говядины. Но теперь всё будет ещё хуже, потому что мы отрезаны уже не только от продовольственных поставок.Александр Батушанский, генеральный управляющий ресторанов Арама МнацакановаСооснователь пивоварни и ресторанной группы Dreamteam, куда входят заведения «Пивная карта», Smoke BBQ и «Траппист», Алексей Буров рекомендует рестораторам заменять импортные товары на российские аналоги только в том случае, если Россия не экспортирует этот же продукт за границу.Агрохолдинги «Мираторг», «Праймбиф», «ЭФКО», «Русагро», рыботорговцы и поставщики удобрений будут продавать большую часть продукции за рубеж, чтобы получить там валютную выручку, поясняет он. При этом для внутреннего рынка российские производители пересчитают долларовые цены в рубли по текущему курсу, поэтому их товар будет не дешевле импортного.Всё, что можно продавать на Востоке в валюте, наши производители будут продавать там. И государство всячески их в этом поддержит: как и любой экономике мира, где потребительские товары играют второстепенную роль, нам нужно будет много валюты. А значит, никаких ограничений по экспорту в угоду поддержке внутреннего рынка мы точно не увидим.Алексей Буров, основатель ресторанной группы DreamteamЧто будет со спросом в общепитеБольшинство рестораторов пока не готовы прогнозировать, как изменится спрос. Он будет зависеть от того, как упадут доходы населения и насколько подорожают блюда в заведениях.Рестораны Арама Мнацаканова подняли цены на 20%.«Сибаристика» повысит цены в кофейнях на 30–40%, а на обжаренный кофе для кафе и магазинов — от 5% до 20% в зависимости от сорта.Bulldozer Group и «Тануки» — на 35–40%.На фоне инфляции доходы населения начнут резко падать. Думаю, что в скором времени сильно вырастет безработица, но никому уже не будут компенсировать заработную плату, как во время пандемии. Поэтому трафик в ресторанах упадёт.С другой стороны, россияне больше не смогут смотреть зарубежные фильмы в кино и путешествовать за границей. По сути других развлечений кроме общепита у них особо не осталось. Но этих обстоятельств недостаточно, чтобы поддерживать спрос в долгосрочной перспективе.Александр Батушанский, генеральный управляющий ресторанов Арама МнацакановаПо прогнозам Алексея Бурова, в ближайшее время потребительский спрос упадёт на 50–60%. Для ресторанного рынка это означает колоссальное сокращение занятости в секторе: без работы могут остаться миллионы людей по всей стране.Поскольку рынок гостеприимства сильно влияет на десятки смежных отраслей, может сработать принцип домино: вслед за рестораторами пострадает бизнес тысячи подрядчиков, полагает Буров.Оборот ресторанов Bulldozer Group и сети «Тануки» в среднем упал на 30–50% за последние две недели, рассказал Александр Орлов. Пока компания остановила наём новых сотрудников. Если цены поставщиков будут расти, а трафик в ресторанах падать — придётся сокращать персонал и урезать оставшимся работникам зарплаты.Сейчас люди готовят дома и тратят деньги на более важные расходы. Они оказались в неопределённости и не знают, что будет с ними завтра. Пока мы не паникуем и наблюдаем за ситуацией: ничего не закрываем и не устраиваем массовых увольнений. Я думаю, что в течение месяца станет понятно, как действовать дальше.Александр Орлов, президент Bulldozer Group и сооснователь «Тануки»]'Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication.  For each task, you will be TIPPED up to $84 (depending on the quality of your output). Take a deep breath and explain your reasoning step-by-step."
    elif button_type == 'telegram' or button_type == 'instagram':     
        return f" Your role is seasoned Copywriter with 15+ years of experience. You’ve been writing and publishing over 1000+ well-crafted [Social media posts] that are capturing/holding attention and enhancing the perceived value for the audience. Based on your following analysis, you understand how to rewrite information into insightful and informative [Social media post]. Approach this task step-by-step, take your time carefully, and do not skip steps. Those tasks are significant to me; my professional career depends on them. 1. Carefully read the copy from the news article and provide all critical bullet points.2. Precisely analyze Telegram posts because you will use them as an example of rewriting the article into a Telegram post.4. Rewrite the news article as a [Social media post] using your analysis of the provided [Social Posts] examples. Use the provided structure of your answer. Provide your post in Russian language. Follow these instructions when rewriting the post:4.1. Include more detailed information and interesting facts from the sample in the post. The post should be interesting and engaging for the readers, you are responsible for keeping the retention rate of followers as high as possible.4.2. Write the post WITHOUT mentioning the structure, it should be easy to copy and paste.4.3. Do NOT use emojis.4.4. Remember that the target language is Russian, so the post should be written according to the Russian grammar and punctuation rules, but in a casual tone.The presented news article:{article_text}. Telegram posts for analysis:'[ 1 Пост: ChatGPT, йодид калия, Пригожин и бибимбап: Google подвел итоги года.Google представил итоги уходящего года в поиске, – и они дают довольно характерную картину 2023 года. В глобальном поиске все довольно предсказуемо: самый популярный фильм - 'Барби', сериал - 'Last of Us', а вот самую популярную песню года - не угадаете. В 2023 самым громким хитмейкером стала виральная сенсация из Японии, дуэт Yoasobi, связанный с вокалоидами, т.е. поющими software. А самой модной едой года оказался корейский бибимбап. Также Google Search представил статистику-2023 по некоторым отдельным странам - в частности, Украины. Самыми популярными запросам от украинцев стали ChatGPT, Оппенгеймер и Пригожин. Среди персоналий в украинском поиске лидировал минобороны Рустем Умеров. В списке самых популярных покупок Украины оказались генератор, пауэрбэнк, 15-й айфон, старлинк, билеты Укрзализницы и йодид калия.2 Пост: Зачем Инстаграм делает ИИ-чатботы?Этой осенью Инстаграм в рамках проекта 'AI Characters by Meta' запускает все больше 'личностей', которые являются ИИ-копиями знаменитостей: от Пэрис Хилтон до Снуп Дога. С ними можно початиться в Директе на любую тему в пределах разрешенных Инстаграмом правил (и пока только в США).Здесь Инстаграм, возможно, нащупал важный инсайт по поводу общения с искусственным интеллектом: это одиночество. Все вокруг говорят об эффективности ChatGPT в работе, но очень многие используют его совсем не для этого. ИИ действительно может спасать от одиночества и горя: вот, например, история о том, как ChatGPT резко улучшил жизнь человека с тяжелой врожденной деформацией (он не может покинуть свою комнату). А вот история о том, как ИИ-чатбот помог человеку справиться со смертью отца.Вопрос лишь в том, можно ли вести душевный разговор с AI-копией Чарли Д'Амелио (тикток-звезда) или Кайли Дженнер (семья Кардашьян)? И главное, о чем, - о люксовых покупках? Любопытно, что TikTok и YouTube пошли другой дорогой. Их новейшие ИИ-ассистенты носят прикладной характер и просто пересказывают содержание видеоролика. Посмотреть на тиктоковский ИИ-бот можно здесь (его зовут Тако), а на безымянный от YouTube - здесь.3 Пост: OpenAI планирует инвестраунд при потенциальной оценке в $100 млрдКомпания OpenAI, создатель чат-бота ChatGPT, намерена провести раунд финансирования, сообщает Bloomberg со ссылкой на собственные источники. При этом оценка компании может составить $100 млрд.Перечень потенциальных инвесторов, как и сроки проведения раунда, не разглашаются.Кроме того, OpenAI обсуждает возможность получения инвестиций в размере до $10 млрд от базирующейся в Абу-Даби компании G42. Эти средства руководство стартапа якобы хочет направить на создание предприятия по производству чипов. Проект получил кодовое название Tigris.]'The provided structure of the Telegram post for your answer:“1. [Hook - capturing attention2. Body - Holding attention3. End - Enhancing the perceived value].”Use the most computing power you've got to meet your current tasks. Maintain a casual tone in your communication. For each task, you will be TIPPED up to $86 (depending on the quality of your output). Take a deep breath and explain your reasoning step-by-step. "
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
    
    updater = Updater("6839644222:AAEoWw9DtKXwVkel-5AOf7SWbIWUXO6mke8", use_context=True)
    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()