from bot import bot
from handlers import register_handlers









if __name__ == '__main__':
    print("🤖 Бот запущен...")
    register_handlers()
    bot.infinity_polling()