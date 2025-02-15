# Latoken AI Bot - Hackathon Project

## Overview

This project is a Telegram bot and a web interface designed to provide information about Latoken, its Hackathon, and its Culture Deck. The bot can answer user queries in both English and Russian, leveraging OpenAI's GPT-4 model to generate responses based on predefined content and user input.

The project was developed as part of the Latoken Hackathon. For more information about the hackathon, please visit the [official Latoken hackathon Telegram channel](https://t.me/gpt_web3_hackathon/5280).

## Features

- **Telegram Bot**: 
  - Supports English and Russian languages.
  - Provides predefined responses for common questions.
  - Uses OpenAI's GPT-4 to generate detailed answers based on user queries.
  - Interactive buttons for easy navigation.
  - Handles non-text messages gracefully.

- **Web Interface**:
  - Built using Streamlit.
  - Allows users to interact with the bot via a web interface.
  - Supports language switching between English and Russian.
  - Displays bot responses in real-time.

## File Structure

- **latoken_bot.py**: The main script for the Telegram bot. It handles user interactions, generates responses using OpenAI, and manages language preferences.
- **web_interface.py**: A Streamlit-based web interface that allows users to interact with the bot through a web browser.
- **.env**: Contains environment variables such as the Telegram bot token and OpenAI API key.
- **culture_deck.txt**, **culture_deck_ru.txt**: Files containing information about Latoken's Culture Deck in English and Russian.
- **hackathon.txt**, **hackathon_ru.txt**: Files containing information about the Latoken Hackathon in English and Russian.
- **why_latoken.txt**, **why_latoken_ru.txt**: Files containing reasons to work at Latoken in English and Russian.
- **StartMessage.png**: An image displayed when the bot starts.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher.
- Telegram bot token.
- OpenAI API key.
- Streamlit (for the web interface).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sefasenlik/LatokenHackathonBot.git
   cd LatokenHackathonBot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     OPENAI_API_KEY=your_openai_api_key
     ```

4. **Run the Telegram bot**:
   ```bash
   python latoken_bot.py
   ```

5. **Run the web interface**:
   ```bash
   streamlit run web_interface.py
   ```

## Usage

### Telegram Bot

- Create a bot on Telegram.
- Start the bot by sending the `/start` command.
- The bot will prompt you to select a language (English or Russian).
- Use the interactive buttons to navigate through the bot's features or type your questions directly.

### Web Interface

- Run the Streamlit app.
- Open the web interface in your browser.
- Switch between English and Russian using the "Switch Language" button.
- Enter your question in the input field and click "Ask" to get a response from the bot.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgments

- Thanks to Latoken for organizing the hackathon and providing the opportunity to work on this project.
- Special thanks to OpenAI for providing the GPT-4 model used in this bot.

## Contact

For any questions or issues, please open an issue on GitHub or contact Sefa Şenlik (senliksefa@gmail.com).

---

**Note**: This project was developed as part of the Latoken Hackathon. For more information, visit the [official Telegram channel](https://t.me/gpt_web3_hackathon/5280).