import os
import telebot
import re
import random
from deep_translator import GoogleTranslator

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

translator = GoogleTranslator(source='en', target='ru')

def check_numerals(line_to_check):
    has_digit = bool(re.search(r'\d', line_to_check))
    return has_digit

def send_daily_notification():
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Missing environment variables.")
        return

    bot = telebot.TeleBot(BOT_TOKEN)
    ru_predictions = set()
    with open('eng_predictions_index.txt', 'r') as file:
        lines = file.readlines()
        while len(ru_predictions) < 3:
            i = random.randint(0, 322293)
            predict = lines[i]
            a = re.match(r"(?P<index>\w+([0-9]*\.)*:)\s(?P<prediction>[\s\w\-,';]+\.)", predict)
            if a:
                index, prediction = a.group('index'), a.group('prediction')
                if len(prediction) > 10 and not check_numerals(prediction):
                    translated = translator.translate(prediction)
                    ru_predictions.add(translated)
    message_text = '\n'.join(ru_predictions)

    try:
        bot.send_message(CHAT_ID, message_text)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")


if __name__ == "__main__":
    send_daily_notification()
