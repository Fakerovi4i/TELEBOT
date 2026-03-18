import telebot
from telebot.types import Message
from telebot import apihelper

PROXY = 'http://user378530:ybn81k@185.121.227.116:7255'
apihelper.proxy = {'https': PROXY}

bot = telebot.TeleBot("8175061257:AAGEy_A1ruOhFYcjj4QKn4HWeAw3bNpZv_0")

@bot.message_handler(commands=['start'])
def start_message(message:Message):
    bot.reply_to(message, "Бот активирован!")


if __name__ == '__main__':
    bot.infinity_polling()
