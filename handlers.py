from telebot.types import Message
from bot import bot
from keyboards import keyboard_main_menu

def register_handlers():
    """Регистрация обработчиков"""

    @bot.message_handler(commands=['start'])
    def start_message(message: Message):
        bot.send_message(
            message.chat.id,
            "🎬 Привет! Я помогу найти фильм.\n"
            "Используй /help для списка команд",
            reply_markup=keyboard_main_menu
        )

    @bot.message_handler(commands=['help'])
    def help_message(message: Message):
        help_text = """
        📋 Доступные команды:
        /start - Начать работу
        /search - Поиск фильма по названию
        /genre - Фильмы по жанру
        /top - Топ фильмов
        """
        bot.send_message(message.chat.id, help_text)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message: Message):
        bot.send_message(message.chat.id, message.text)