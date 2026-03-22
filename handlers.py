from typing import List, Dict, Any
import json
from telebot.types import Message

from bot import bot
from keyboards import main_menu_keyboard, list_films_keyboard, filters_keyboard, choice_rating_keyboard
from api_requests import find_move_by_name, get_movie_by_id, find_movies_by_rating
from my_states import ChoiceFilters




def info_about_move(data: Dict[str, Any]):
    print(json.dumps(data, ensure_ascii=False, indent=2))
    name = data["name"]
    poster = data["poster"]["previewUrl"]
    kp_rate = data["rating"]["kp"]
    year = data["year"]
    countries = data["countries"][0]["name"]
    description = data.get("description", None)
    if "watchability" not in data:
        url = url_ivi = url_okko = None
    else:
        url = data["watchability"]["items"][0]["url"]


    return name, poster, kp_rate, year, countries, url, description


def process_find_move(message: Message):
        name = message.text
        result = find_move_by_name(name)
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        if result is None:
            bot.send_message(message.chat.id, 'Произошла ошибка обращения к сайту!\nПопробуйте позже.', reply_markup=main_menu_keyboard())
            return
        if len(result) == 0:
            bot.send_message(message.chat.id, 'Ничего не найдено!', reply_markup=main_menu_keyboard())
            return

        try:
            bot.send_message(message.chat.id,'Список найденных фильмов:\n', reply_markup=list_films_keyboard(result))


        except (KeyError, IndexError) as e:
            bot.send_message(message.chat.id, 'Ошибка при получении данных о фильме!', reply_markup=main_menu_keyboard())


def register_handlers():
    """Регистрация обработчиков"""

    @bot.message_handler(commands=['start'])
    def start_message(message: Message):
        bot.send_message(
            message.chat.id,
            "🎬 Привет! Я помогу найти фильм.\n"
            "Используй /help для списка команд",
            reply_markup=main_menu_keyboard()
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


    @bot.callback_query_handler(func=lambda call: call.data.startswith("film_"))
    def callback_film_id_handler(call):
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        movie_id = call.data.split("_")[1]
        movie_data = get_movie_by_id(int(movie_id))
        name, poster, kp_rate, year, countries, url, description = info_about_move(movie_data)
        info = f"🎬 {name} | {year} | {countries} | Рейтинг: {kp_rate}"
        if url is None:
            urls_for_watch = "\n\n"
        else:
            urls_for_watch = (f"\n🍿 [Смотреть]({url})\n\n")

        if description is None:
            description = "Описание:\nНет описания."
        else:
            description = f"Описание:\n{description}"

        bot.send_photo(
            call.message.chat.id,
            photo=poster,
            caption=info + urls_for_watch + description,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )


    @bot.message_handler(func=lambda message: message.text == '🧩 Поиск по фильтрам')
    def filters(message: Message):
        bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data.clear()

        bot.send_message(
            message.chat.id,
            "Выберите фильтр:",
            reply_markup=filters_keyboard())


    @bot.callback_query_handler(func=lambda call: call.data == "filters_rating", state=ChoiceFilters.waiting_filters)
    def callback_rating_filter(call):
        """Обработчик нажатия на кнопку 'Рейтинг Кинопоиск'"""
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            "🍿 Выбери минимальный рейтинг:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=choice_rating_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("rating_"), state=ChoiceFilters.waiting_filters)
    def callback_rating_selected(call):
        """Обработчик выбора рейтинга"""
        bot.answer_callback_query(call.id)
        rating = call.data.split("_")[1]  # Получаем значение рейтинга из callback_data

        # Сохраняем выбранный рейтинг в состояние
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['rating'] = rating
            selected_filters = dict(data)

        bot.edit_message_text(
            "Выбрано: ⭐" + rating,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=filters_keyboard(selected_filters=selected_filters)
        )

