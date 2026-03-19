from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup



def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔍 Поиск фильма", "🎭 По жанру")
    keyboard.add("⭐ Топ фильмов", "ℹ️ Помощь")
    return keyboard


# def get_genre_keyboard():
#     """Клавиатура с жанрами"""
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     genres = [
#         ("🎬 Боевик", "genre_боевик"),
#         ("😂 Комедия", "genre_комедия"),
#         ("😱 Ужасы", "genre_ужасы"),
#         ("💕 Мелодрама", "genre_мелодрама"),
#         ("🔫 Триллер", "genre_триллер"),
#         ("🚀 Фантастика", "genre_фантастика"),
#     ]
#
#     buttons = [InlineKeyboardButton(text=name, callback_data=data)
#                for name, data in genres]
#     keyboard.add(*buttons)
#     return keyboard


keyboard_main_menu = main_menu_keyboard()