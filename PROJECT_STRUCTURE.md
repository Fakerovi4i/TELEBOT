# 📁 Структура проекта Telegram-бота с Кинопоиск API

## 🎯 Рекомендуемая структура файлов

```
D:/My_python/Telebot_final/
├── main.py              # ← Точка входа (запуск бота)
├── bot.py               # ← Инициализация бота
├── config.py            # ← Конфигурация (токены, настройки)
├── handlers.py          # ← Обработчики команд и сообщений
├── keyboards.py         # ← Клавиатуры (inline, reply)
├── api_requests.py      # ← Запросы к Кинопоиск API
├── database.py          # ← Работа с БД (опционально)
├── utils.py             # ← Вспомогательные функции
└── .env                 # ← Секретные данные
```

---

## 📝 Назначение каждого файла

### 1️⃣ **main.py** — Точка входа (запуск бота)
**Что делает:** Запускает бота и регистрирует обработчики

```python
from bot import bot_instance
from handlers import register_handlers

if __name__ == '__main__':
   print("🤖 Бот запущен...")
   register_handlers(bot_instance)
   bot_instance.infinity_polling()
```

**Запуск:** `python main.py`

---

### 2️⃣ **bot.py** — Инициализация бота
**Что делает:** Создаёт экземпляр бота, настраивает прокси

```python
import telebot
from telebot import apihelper
from config import BOT_TOKEN, PROXY

# Настройка прокси (если нужен)
if PROXY:
    apihelper.proxy = {'https': PROXY}

# Создание экземпляра бота
bot = telebot.TeleBot(BOT_TOKEN)
```

**Важно:** Только инициализация, никаких обработчиков!

---

### 3️⃣ **handlers.py** — Обработчики команд
**Что делает:** Вся логика обработки команд и сообщений пользователя

**Основные функции:**
- Обработка команд (`/start`, `/help`, `/search`, `/genre`, `/top`)
- Обработка callback-кнопок (inline клавиатуры)
- Обработка текстовых сообщений
- Регистрация всех обработчиков

**Пример структуры:**

```python
from telebot.types import Message, CallbackQuery
from bot import bot_instance
from keyboards import main_menu_keyboard, get_genre_keyboard
from api_requests import search_movie_by_name, get_movie_by_genre


def register_handlers(bot_instance):
   """Регистрация всех обработчиков"""

   @bot_instance.message_handler(commands=['start'])
   def start_message(message: Message):
      # Логика команды /start
      pass

   @bot_instance.message_handler(commands=['search'])
   def search_command(message: Message):
      # Логика поиска фильма
      pass

   @bot_instance.callback_query_handler(func=lambda call: True)
   def callback_handler(call: CallbackQuery):
      # Обработка нажатий на inline кнопки
      pass
```

---

### 4️⃣ **api_requests.py** — Запросы к Кинопоиск API
**Что делает:** Вся работа с внешним API Кинопоиска

**Основные функции:**
- `search_movie_by_name(movie_name)` — поиск по названию
- `get_movie_by_genre(genre)` — фильмы по жанру
- `get_top_movies(limit)` — топ фильмов
- `get_movie_details(movie_id)` — детали фильма

**Пример функции:**
```python
import requests
from config import API_HOST, SITE_API_KEY, API_TIMEOUT

def search_movie_by_name(movie_name: str):
    """Поиск фильма по названию"""
    try:
        url = f"{API_HOST}/movie/search"
        headers = {"X-API-KEY": SITE_API_KEY}
        params = {"query": movie_name, "limit": 10}

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )

        if response.status_code == 200:
            return response.json().get('docs', [])
        return []

    except requests.Timeout:
        print("⏰ Превышено время ожидания")
        return []
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []
```

---

### 5️⃣ **keyboards.py** — Клавиатуры
**Что делает:** Создаёт все клавиатуры для бота

**Основные функции:**
- `main_menu_keyboard()` — главное меню (ReplyKeyboard)
- `get_genre_keyboard()` — выбор жанра (InlineKeyboard)
- `get_movie_actions()` — действия с фильмом (InlineKeyboard)

**Пример:**
```python
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔍 Поиск фильма", "🎭 По жанру")
    keyboard.add("⭐ Топ фильмов", "ℹ️ Помощь")
    return keyboard

def get_genre_keyboard():
    """Клавиатура с жанрами"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    genres = [
        ("🎬 Боевик", "genre_боевик"),
        ("😂 Комедия", "genre_комедия"),
        ("😱 Ужасы", "genre_ужасы"),
    ]
    buttons = [InlineKeyboardButton(text=name, callback_data=data)
               for name, data in genres]
    keyboard.add(*buttons)
    return keyboard
```

---

### 6️⃣ **config.py** — Конфигурация
**Что делает:** Хранит все настройки и секретные данные

```python
import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

# Секретные данные из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_API_KEY = os.getenv("SITE_API_KEY")
PROXY = os.getenv("PROXY")

# Публичные константы
API_HOST = "https://api.kinopoisk.dev/v1.4"
API_TIMEOUT = 10  # секунды
```

---

### 7️⃣ **utils.py** — Вспомогательные функции (опционально)
**Что делает:** Общие функции, используемые в разных частях проекта

**Примеры функций:**
- Форматирование текста фильма
- Валидация данных
- Логирование
- Обработка ошибок

```python
def format_movie_info(movie: dict) -> str:
    """Форматирует информацию о фильме для отправки пользователю"""
    return (
        f"🎬 {movie.get('name', 'Без названия')}\n"
        f"⭐ Рейтинг: {movie.get('rating', {}).get('kp', 'N/A')}\n"
        f"📅 Год: {movie.get('year', 'N/A')}\n"
        f"🎭 Жанр: {', '.join(movie.get('genres', []))}\n"
    )
```

---

## 🎯 Логика работы файлов

| Файл | Ответственность | Импортирует | Экспортирует |
|------|----------------|-------------|--------------|
| **main.py** | Запуск бота | bot, handlers | - |
| **bot.py** | Создание бота | config | bot |
| **handlers.py** | Обработка команд | bot, keyboards, api_requests | register_handlers |
| **api_requests.py** | Работа с API | config | функции запросов |
| **keyboards.py** | Создание кнопок | telebot.types | функции клавиатур |
| **config.py** | Настройки | os, dotenv | константы |

---

## ✅ Преимущества такой структуры

1. ✅ **Разделение ответственности** — каждый файл делает одно дело
2. ✅ **Легко найти код** — знаешь где искать нужную функцию
3. ✅ **Легко тестировать** — можно тестировать API отдельно от бота
4. ✅ **Легко расширять** — добавил новый handler, не трогая остальное
5. ✅ **Профессионально** — так организованы реальные проекты

---

## 🔄 Поток выполнения

```
1. main.py запускается
   ↓
2. Импортирует bot из bot.py
   ↓
3. bot.py создаёт экземпляр бота (использует config.py)
   ↓
4. main.py вызывает register_handlers() из handlers.py
   ↓
5. handlers.py регистрирует все обработчики
   ↓
6. Обработчики используют:
   - keyboards.py для создания кнопок
   - api_requests.py для запросов к Кинопоиску
   ↓
7. bot.infinity_polling() запускает бота
```

---

## 💡 Ответы на вопросы

### ❓ Где происходит основная обработка кода?

**Да, правильно понял!** Основная логика в двух файлах:

1. **handlers.py** — обработка действий пользователя
   - Что делать при команде `/start`
   - Как реагировать на кнопки
   - Как обрабатывать текстовые сообщения

2. **api_requests.py** — работа с данными Кинопоиска
   - Как искать фильмы
   - Как получать топ
   - Как фильтровать по жанрам

**Остальные файлы — вспомогательные:**
- `bot.py` — просто создаёт бота
- `keyboards.py` — просто создаёт кнопки
- `config.py` — просто хранит настройки
- `main.py` — просто запускает всё

---

## 🚀 Пример взаимодействия файлов

**Пользователь нажал кнопку "🔍 Поиск фильма":**

```
1. handlers.py получает сообщение
   ↓
2. Отправляет клавиатуру из keyboards.py
   ↓
3. Пользователь вводит название
   ↓
4. handlers.py вызывает search_movie_by_name() из api_requests.py
   ↓
5. api_requests.py делает запрос к Кинопоиску (использует config.py)
   ↓
6. Возвращает данные в handlers.py
   ↓
7. handlers.py форматирует и отправляет пользователю
```

---

*Создано для учебного проекта Telegram-бота с Кинопоиск API*
