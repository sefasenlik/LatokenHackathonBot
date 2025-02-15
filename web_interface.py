import streamlit as st
from latoken_bot import generate_response_from_files  # Import your bot's response generation function

# Initialize the session state for language if it doesn't exist
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default to English

# Add a button to toggle language
if st.button("Switch Language • Сменить язык"):
    st.session_state.language = 'ru' if st.session_state.language == 'en' else 'en'

# Update the interface text based on the selected language
if st.session_state.language == 'ru':
    st.title("🤖 Latoken ИИ-бот")
    st.write("Добро пожаловать в ИИ-бот Latoken! Спросите меня обо всем, что касается Latoken, хакатона или Culture Deck.")
    user_input_label = "Введите свой вопрос:"
    button_label = "Спросить"
    response_label = "Ответ бота:"
else:
    st.title("🤖 Latoken AI Bot")
    st.write("Welcome to the Latoken AI Bot! Ask me anything about Latoken, the Hackathon, or the Culture Deck.")
    user_input_label = "Enter your question:"
    button_label = "Ask"
    response_label = "Bot's Response:"

# Input field for user questions
user_input = st.text_input(user_input_label)

# Button to submit the question
if st.button(button_label):
    if user_input:
        # Generate the bot's response using your existing function
        bot_response = generate_response_from_files(user_input, st.session_state.language)  # Use selected language
        st.write(f"**{response_label}**")
        st.write(bot_response)
    else:
        st.write(user_input_label)