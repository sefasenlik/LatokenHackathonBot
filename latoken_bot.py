from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
from openai import OpenAI
from dotenv import load_dotenv
from langdetect import detect

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Predefined responses in English and Russian
RESPONSES = {
    "en": {
        "What is latoken?": "Latoken is a cryptocurrency exchange platform that focuses on tokenizing assets and providing liquidity for new tokens.",
        "What is the Latoken Hackathon?": "The Latoken Hackathon is an event where developers compete to create innovative solutions based on AI and Web3. It's a great opportunity to showcase your skills and win prizes.",
        "How can I participate in the Hackathon?": "To participate in the Latoken Hackathon, visit their official website and follow the registration instructions.",
        "What are the benefits of working at Latoken?": "Working at Latoken offers opportunities to work on cutting-edge blockchain technology, a dynamic work environment, and competitive benefits.",
    },
    "ru": {
        "Что такое Latoken?": "Latoken — это платформа для обмена криптовалютой, которая занимается токенизацией активов и предоставлением ликвидности для новых токенов.",
        "Что такое хакатон Latoken?": "Хакатон Latoken — это мероприятие, на котором разработчики соревнуются в создании инновационных решений на основе AI и Web3. Это отличная возможность продемонстрировать свои навыки и выиграть призы.",
        "Как я могу участвовать в хакатоне?": "Чтобы принять участие в хакатоне Latoken, посетите их официальный сайт и следуйте инструкциям по регистрации.",
        "Какие преимущества работы в Latoken?": "Работа в Latoken предлагает возможности работать с передовыми блокчейн-технологиями, динамичной рабочей средой и конкурентоспособными льготами.",
    },
}

# Load all files into memory
def load_files():
    files = {
        "culture_deck_en": "culture_deck.txt",
        "culture_deck_ru": "culture_deck_ru.txt",
        "hackathon_en": "hackathon.txt",
        "hackathon_ru": "hackathon_ru.txt",
        "why_latoken_en": "why_latoken.txt",
        "why_latoken_ru": "why_latoken_ru.txt",
    }
    content = {}
    for key, file_name in files.items():
        try:
            with open("resources\\"+file_name, "r", encoding="utf-8") as file:
                content[key] = file.read()
        except FileNotFoundError:
            content[key] = ""  # If a file is missing, use an empty string
    return content

FILE_CONTENT = load_files()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send the image
    with open("StartMessage.png", "rb") as photo:
        await update.message.reply_photo(photo=InputFile(photo))

    # Send Russian welcome message
    await update.message.reply_text(
        "*RU* Бот-помощник хакатона 🤖\n\n"
        "Привет! Я здесь, чтобы помочь вам узнать о Latoken, о нашем хакатоне и Culture Deck. Задайте мне любой вопрос! ☝️🤓",
        parse_mode="Markdown"
    )

    # Send English welcome message
    await update.message.reply_text(
        "*EN* Hackathon Help Bot 🤖\n\n"
        "Hello! I'm here to help you learn about Latoken, our Hackathon, and Culture Deck. Ask me anything! ☝️🤓",
        parse_mode="Markdown"
    )

    # Ask for language preference
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "*RU* Пожалуйста, выберите предпочитаемый язык:\n"
        "*EN* Please select your preferred language:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Detect language from user context or default to English
    language = context.user_data.get('language', 'en')
    
    # Create FAQ buttons
    keyboard = []
    responses = RESPONSES["ru" if language == "ru" else "en"]
    for question in responses.keys():
        keyboard.append([InlineKeyboardButton(question, callback_data=f"faq_{question}")])
    
    # Add main menu button
    keyboard.append([InlineKeyboardButton(
        "Main Menu" if language == "en" else "Главное меню",
        callback_data="main_menu"
    )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Help message explaining how the bot works
    help_text = {
        "en": (
            "*Frequently Asked Questions:*\n\n"
            "Below you'll find common questions about Latoken and the hackathon.\n\n"
            "*How to use this bot:*\n"
            "1. Click any button to get predefined answers\n"
            "2. Or simply type your question in English or Russian\n"
            "3. The bot will respond based on Latoken's documentation\n"
            "4. You can always return to the main menu using the button below"
        ),
        "ru": (
            "*Часто задаваемые вопросы:*\n\n"
            "Ниже вы найдете популярные вопросы о Latoken и хакатоне.\n\n"
            "*Как использовать этого бота:*\n"
            "1. Нажмите любую кнопку для получения готовых ответов\n"
            "2. Или просто напишите свой вопрос на русском или английском\n"
            "3. Бот ответит на основе документации Latoken\n"
            "4. Вы всегда можете вернуться в главное меню, используя кнопку ниже"
        )
    }
    
    await update.message.reply_text(
        help_text[language],
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle language selection
    if query.data.startswith("lang_"):
        language = query.data.split("_")[1]
        context.user_data['language'] = language
        await show_main_menu_after_language(query, language)
        return

    # Handle FAQ responses
    if query.data.startswith("faq_"):
        language = context.user_data.get('language', 'en')
        question = query.data[4:]  # Remove 'faq_' prefix
        response = RESPONSES["ru" if language == "ru" else "en"].get(question)
        if response:
            await query.edit_message_text(
                response,
                parse_mode="Markdown"
            )
            await show_main_menu(query, language)
        return

    # Get user's language preference (English is the default language)
    language = context.user_data.get('language', 'en')
    
    # Handle other buttons based on selected language
    if query.data == "about_latoken":
        message = {
            "en": "Latoken is a cryptocurrency exchange platform that focuses on tokenizing assets and providing liquidity for new tokens. Visit [our website](https://coda.io/@latoken/latoken-talent/latoken-161) and dive into the world of Latoken.",
            "ru": "Latoken - это платформа для обмена криптовалют, которая специализируется на токенизации активов и обеспечении ликвидности для новых токенов. Посетите [наш сайт](https://coda.io/@latoken/latoken-talent/latoken-161) и окунитесь в мир Latoken."
        }

        await query.edit_message_text(
            message[language],
            parse_mode="Markdown"
        )
        await show_main_menu(query, language)

    elif query.data == "hackathon_info":
        keyboard = [
            [InlineKeyboardButton(
                "Hackathon Content" if language == "en" else "Описание хакатона", 
                callback_data="hackathon_content"
            )],
            [InlineKeyboardButton(
                "Schedule" if language == "en" else "Расписание", 
                callback_data="hackathon_schedule"
            )],
            [InlineKeyboardButton(
                "Main Menu" if language == "en" else "Главное меню", 
                callback_data="main_menu"
            )],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = {
            "en": "Choose an option to learn more about the hackathon:",
            "ru": "Выберите опцию для получения дополнительной информации о хакатоне:"
        }
        await query.edit_message_text(
            message[language],
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif query.data == "hackathon_content":
        message = {
            "en": "The hackathon starts on Friday at 18:00. Latoken officials will introduce themselves and present the tasks. Participants can choose tasks based on their interests and skills. You'll have 23 hours to complete your project and upload it by 17:00 the next day. If your project is accepted, you'll present it at 18:00 on Saturday.\n\nAre you ready to take on the challenge? Check our [discussion channel](https://t.me/gpt_web3_hackathon/1/10091) to learn more.",
            "ru": "Хакатон начнется в пятницу в 18:00. Представители Latoken представятся и расскажут о задачах. Участники смогут выбрать задачи в соответствии со своими интересами и навыками. У вас будет 23 часа на выполнение проекта и его загрузку до 17:00 следующего дня. Если ваш проект будет принят, вы представите его в 18:00 в субботу.\n\nВы готовы принять вызов? Посетите наш [канал обсуждения](https://t.me/gpt_web3_hackathon/1/10091), чтобы узнать больше."
        }
        await query.edit_message_text(
            message[language],
            parse_mode="Markdown"
        )
        await show_main_menu(query, language)

    elif query.data == "hackathon_schedule":
        message = {
            "en": "**Hackathon Schedule:**\n\n"
                "📅 **Friday 18:00** → Introduction & Task Distribution\n"
                "📅 **Saturday 17:00** → Task Solution Submission\n"
                "📅 **Saturday 18:00** → Solution Demonstrations\n\n"
                "Please [register](https://calendly.com/latoken-career-events/ai-hackathon) and [join](https://discord.gg/2YrRvWjRTD) our live event to find out more details.",
            "ru": "**Расписание хакатона:**\n\n"
                "📅 **Пятница 18:00** → Введение и распределение задач\n"
                "📅 **Суббота 17:00** → Сдача решений задач\n"
                "📅 **Суббота 18:00** → Демонстрация решений\n\n"
                "Пожалуйста, [зарегистрируйтесь](https://calendly.com/latoken-career-events/ai-hackathon) и [присоединяйтесь](https://discord.gg/2YrRvWjRTD) к нашей встрече, чтобы узнать подробности."
        }
        await query.edit_message_text(
            message[language],
            parse_mode="Markdown"
        )
        await show_main_menu(query, language)

    elif query.data == "culture_deck":
        message = {
            "en": "The Latoken Culture Deck outlines the company's values, mission, and commitment to innovation. You can read it [here](https://coda.io/@latoken/latoken-talent/culture-139) and ask me your questions.",
            "ru": "Культурный дек Latoken описывает ценности, миссию и приверженность компании инновациям. Вы можете прочитать его [здесь](https://coda.io/@latoken/latoken-talent/culture-139) и задать мне свои вопросы."
        }
        await query.edit_message_text(
            message[language],
            parse_mode="Markdown"
        )
        await show_main_menu(query, language)

    elif query.data == "main_menu":
        await show_main_menu(query, language)

# Update show_main_menu to handle both cases
async def show_main_menu(query, language, edit_message=False):
    keyboard = [
        [InlineKeyboardButton(
            "About Latoken" if language == "en" else "О Латокене", 
            callback_data="about_latoken"
        )],
        [InlineKeyboardButton(
            "Hackathon Info" if language == "en" else "Инфо о хакатоне", 
            callback_data="hackathon_info"
        )],
        [InlineKeyboardButton(
            "Culture Deck" if language == "en" else "Культурный дек", 
            callback_data="culture_deck"
        )],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = {
        "en": "Pick one of the options below or *type your question*:",
        "ru": "Выберите один из вариантов ниже или *введите свой вопрос*:"
    }

    if edit_message:
        await query.edit_message_text(
            message[language],
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await query.message.reply_text(
            message[language],
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# Simplified function that uses show_main_menu
async def show_main_menu_after_language(query, language):
    await show_main_menu(query, language, edit_message=True)

# Handle non-text messages
async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language', 'en')
    message = {
        "en": "Sorry, I only accept text messages. Please send me a text question.",
        "ru": "Извините, я принимаю только текстовые сообщения. Пожалуйста, задайте мне текстовый вопрос."
    }
    await update.message.reply_text(
        message[language],
        parse_mode="Markdown"
    )

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    language = detect(user_message)  # Detect the language of the user's input

    # Initialize conversation context if not exists
    if 'last_bot_message' not in context.user_data:
        context.user_data['last_bot_message'] = None

    # Check if the question is in predefined responses
    if language == "ru":
        response = RESPONSES["ru"].get(user_message.lower())
    else:
        response = RESPONSES["en"].get(user_message.lower())

    if response:
        # Add a follow-up question to predefined responses
        follow_up = {
            "en": "\n\nWould you like to know more about this topic?",
            "ru": "\n\nХотите узнать больше об этой теме?"
        }
        response += follow_up["ru" if language == "ru" else "en"]
        context.user_data['last_bot_message'] = response
        await update.message.reply_text(response)
    else:
        # Check if the user's message contains a question mark
        has_question = '?' in user_message

        # Get the last bot message
        last_bot_message = context.user_data.get('last_bot_message')

        # Modify the prompt based on conversation context
        if last_bot_message and not has_question:
            # If user didn't ask a question after bot's question, encourage engagement
            prompt_addition = {
                "en": "The user seems to have ignored the previous question. Acknowledge their response and try to engage them with another question.",
                "ru": "Пользователь, похоже, проигнорировал предыдущий вопрос. Примите во внимание их ответ и попробуйте вовлечь их другим вопросом."
            }
            question = f"{user_message}\n\nContext: {prompt_addition['ru' if language == 'ru' else 'en']}"
        else:
            question = user_message

        response = generate_response_from_files(question, language)
        context.user_data['last_bot_message'] = response
        await update.message.reply_text(response)

# Generate a response using OpenAI and all files
def generate_response_from_files(question, language):
    if language == "ru":
        # Combine all Russian files
        combined_content = (
            FILE_CONTENT["culture_deck_ru"] + "\n\n" +
            FILE_CONTENT["hackathon_ru"] + "\n\n" +
            FILE_CONTENT["why_latoken_ru"]
        )
        system_prompt = (
            "Вы — полезный помощник, который отвечает на вопросы о Latoken, их хакатоне и их Culture Deck. "
            "Всегда заканчивайте свой ответ вопросом (в новой строке), чтобы проверить понимание или узнать больше о интересах пользователя."
        )
    else:
        # Combine all English files
        combined_content = (
            FILE_CONTENT["culture_deck_en"] + "\n\n" +
            FILE_CONTENT["hackathon_en"] + "\n\n" +
            FILE_CONTENT["why_latoken_en"]
        )
        system_prompt = (
            "You are a helpful assistant that answers questions about Latoken, their Hackathon, and their Culture Deck. "
            "Always end your response with a question (in a new line) to check understanding or learn more about user's interests."
        )

    prompt = (
        f"The following is a question about Latoken:\n\n{question}\n\n"
        f"Here is the relevant information:\n\n{combined_content}\n\n"
        f"Please provide a detailed and well-structured answer (maximum 600 characters) to the question, "
        f"ensuring clarity and completeness. End with a relevant follow-up question to engage the user. "
        f"The answer will be displayed through Telegram API with Markdown formatting."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't generate a response. Error: {str(e)}"

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Main function
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))
    app.add_error_handler(error)

    # Start the bot
    print("Polling...")
    app.run_polling(poll_interval=3)