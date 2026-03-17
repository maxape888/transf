import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Твои данные
BOT_TOKEN = '8692941416:AAEw-_MxtWtQ90bm0yfPDAP9WNOZIKHYpN8'
CHANNEL_ID = -1003773336373  # Замени на ID твоего канала (обязательно с минусом)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Напиши свой отзыв или предложение в чат, и я передам его администраторам."
    )

# Обработчик для пересылки отзывов
@dp.message(F.text)
async def handle_review(message: types.Message):
    # Формируем красивый текст для канала
    username = message.from_user.username
    user_link = f"@{username}" if username else message.from_user.first_name
    
    review_text = (
        f"📝 <b>Новый отзыв!</b>\n\n"
        f"👤 От: {user_link}\n"
        f"💬 Текст: {message.text}"
    )

    try:
        # Бот отправляет сформированное сообщение в канал
        await bot.send_message(
            chat_id=CHANNEL_ID, 
            text=review_text, 
            parse_mode="HTML"
        )
        # Отвечаем пользователю, что всё прошло успешно
        await message.answer("Спасибо! Твой отзыв успешно отправлен.")
        
    except Exception as e:
        # Если бот не в канале или ID указан неверно
        await message.answer("Произошла ошибка при отправке отзыва. Попробуйте позже.")
        print(f"Ошибка: {e}")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())