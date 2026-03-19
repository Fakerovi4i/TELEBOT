from telebot.types import Message
from bot import bot
from keyboards import keyboard_main_menu
from api_requests import get_move_by_name


def info_about_move(data: list[dict]):
    name = data[0]["name"]
    poster = data[0]["poster"]["previewUrl"]
    kp_rate = data[0]["rating"]["kp"]
    return name, poster, kp_rate


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

    @bot.message_handler(func=lambda message: message.text in ['/search', '🔍 Поиск фильма'])
    def find_move(message: Message):
        msg = bot.send_message(message.chat.id, "Введите название фильма для поиска:\n")
        bot.register_next_step_handler(msg, process_find_move)

    def process_find_move(message: Message):
        name = message.text
        result = get_move_by_name(name)
        if result is None:
            bot.send_message(message.chat.id, 'Произошла ошибка обращения к сайту!\nПопробуйте позже.', reply_markup=keyboard_main_menu)
            return
        if len(result) == 0:
            bot.send_message(message.chat.id, 'Ничего не найдено!', reply_markup=keyboard_main_menu)
            return

        try:
            movie_name, poster, kp_rate  = info_about_move(result)
            bot.send_photo(
                message.chat.id,
                photo=poster,
                caption=f"""🎬 {movie_name}\nРейтинг КиноПоиск: {kp_rate:.1f}""" #reply_markup = keyboard_main_menu
            )

        except (KeyError, IndexError) as e:
            bot.send_message(message.chat.id, 'Ошибка при получении данных о фильме!', reply_markup=keyboard_main_menu)
