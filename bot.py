import telebot
from telebot import apihelper
from config import BOT_TOKEN, PROXY


apihelper.proxy = {'https': PROXY}
apihelper.READ_TIMEOUT = 60

bot = telebot.TeleBot(BOT_TOKEN, threaded=True, skip_pending=True)



