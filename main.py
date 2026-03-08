import os
from flask import Flask, request
import telebot

# 1. Берем токен из настроек Render
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# 2. Обработчик сообщений от Telegram
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# 3. Настройка вебхука при заходе на главную страницу
@app.route("/")
def webhook_setup():
    # Render сам дает нам адрес через переменную RENDER_EXTERNAL_URL
    url = os.getenv("RENDER_EXTERNAL_URL")
    bot.remove_webhook()
    bot.set_webhook(url=url + '/' + TOKEN)
    return "Вебхук успешно установлен! ✅", 200

# Команда /start для проверки
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ура! Бот работает через вебхук! 🚀")

if __name__ == "__main__":
    # Запуск сервера на порту, который выделит Render
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
