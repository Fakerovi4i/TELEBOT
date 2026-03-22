import telebot
from telebot import apihelper
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config import BOT_TOKEN, PROXY


apihelper.proxy = {'https': PROXY}
apihelper.READ_TIMEOUT = 60


state_storage = StateMemoryStorage()


bot = telebot.TeleBot(BOT_TOKEN, threaded=True, skip_pending=True, state_storage=state_storage)


# Добавление фильтра состояний
bot.add_custom_filter(custom_filters.StateFilter(bot))

