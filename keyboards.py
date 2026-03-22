from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from typing import List, Dict, Any, Optional



def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔍 Поиск фильма", "🎭 По жанру")
    keyboard.add("⭐ Топ фильмов", "🧩 Поиск по фильтрам")
    return keyboard

def list_films_keyboard(films: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    '''Клавиатура с найденными фильмами'''
    keyboard = InlineKeyboardMarkup(row_width=1)
    count = 0
    for film in films:
        count += 1
        keyboard.add(
            InlineKeyboardButton(
                f"""{count}. 🎬{film['name']} | {film['year']} | {film['type']} | {film['countries'][0]['name']}""",
                callback_data=f"film_{film['id']}"))
    return keyboard


def filters_keyboard(selected_filters: Optional[Dict] = None) -> InlineKeyboardMarkup:
    """Клавиатура с фильтрами"""

    if selected_filters is None:
        selected_filters = {}
    keyboard = InlineKeyboardMarkup(row_width=2)

    rating_text = "🍿Рейтинг Кинопоиск"
    if 'rating' in selected_filters:
        rating_text = "✅ " + rating_text

    keyboard.add(
        InlineKeyboardButton("⚡Название✨", callback_data="filters_name"),
        InlineKeyboardButton("🎭Жанр", callback_data="filters_genre"),
        InlineKeyboardButton("🕙Год", callback_data="filters_year"),
        InlineKeyboardButton("🎬Тип(Сериал, фильм, anime)", callback_data="filters_type"),
        InlineKeyboardButton("🇷🇺🇮🇹🇺🇸Страна", callback_data="filters_country"),
        InlineKeyboardButton(rating_text, callback_data="filters_rating"),
        InlineKeyboardButton("❌Выход", callback_data="filters_exit"),
        InlineKeyboardButton("👀Найти", callback_data="filters_find")

    )
    return keyboard


def choice_rating_keyboard():
    """Клавиатура выбора рейтинга от 5 до 10"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("⭐ 5", callback_data="rating_5"),
        InlineKeyboardButton("⭐ 6", callback_data="rating_6"),
        InlineKeyboardButton("⭐ 7", callback_data="rating_7"),
        InlineKeyboardButton("⭐ 8", callback_data="rating_8"),
        InlineKeyboardButton("⭐ 9", callback_data="rating_9"),
        InlineKeyboardButton("⭐ 10", callback_data="rating_10")
    )
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




