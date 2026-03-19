import telebot
from telebot import apihelper
from config import BOT_TOKEN, PROXY


apihelper.proxy = {'https': PROXY}

bot = telebot.TeleBot(BOT_TOKEN)



