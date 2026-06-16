import os
import telebot
import re
import random
from deep_translator import GoogleTranslator

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

translator = GoogleTranslator(source='en', target='ru')

USERS_FILE = 'users.txt'

def append_user_id(user_id):
    # Создаем файл, если он не существует
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            pass

    # Читаем текущих пользователей, чтобы избежать дубликатов
    with open(USERS_FILE, 'r') as f:
        existing_users = [line.strip() for line in f]

    # Если пользователя нет в списке, добавляем его
    if str(user_id) not in existing_users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")
        return True
    return False


@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    is_new = append_user_id(chat_id)

    if is_new:
        bot.reply_to(message, "Вы успешно подписались на рассылку!")
    else:
        bot.reply_to(message, "Вы уже подписаны на рассылку.")

def check_numerals(line_to_check):
    has_digit = bool(re.search(r'\d', line_to_check))
    return has_digit

def send_daily_notification():
    if not BOT_TOKEN:
        print("Error: Missing environment variables.")
        return

    users_file = 'users.txt'

    if not os.path.exists(users_file):
        print("Файл с пользователями не найден.")
        return

    with open(users_file, 'r') as f:
        # Убираем пустые строки и пробелы
        users = [line.strip() for line in f if line.strip()]


    for user_id in users:
        ru_predictions = set()
        with open('eng_predictions_index.txt', 'r') as file:
            lines = file.readlines()
            while len(ru_predictions) < 3:
                i = random.randint(0, 32293)
                predict = lines[i]
                a = re.match(r"(?P<index>\w+([0-9]*\.)*:)\s(?P<prediction>[\s\w\-,';]+\.)", predict)
                if a:
                    index, prediction = a.group('index'), a.group('prediction')
                    if len(prediction) > 10 and not check_numerals(prediction):
                        translated = translator.translate(prediction)
                        ru_predictions.add(translated)
        message_text = '\n'.join(ru_predictions)

        try:
            bot.send_message(user_id, message_text)
            print("Message sent successfully!")
        except Exception as e:
            print(f"Failed to send message: {e}")


if __name__ == "__main__":
    send_daily_notification()
