import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Включаем логирование, чтобы видеть отчеты о работе в консоли Railway
logging.basicConfig(level=logging.INFO)

# Получаем данные из переменных окружения (Environment Variables)
# На Railway тебе нужно будет создать переменные с этими именами
BOT_TOKEN = os.getenv('BOT_TOKEN')
raw_channel_id = os.getenv('CHANNEL_ID')

# Проверка, что переменные заданы, чтобы бот не упал с непонятной ошибкой
if not BOT_TOKEN:
    exit("Ошибка: Переменная BOT_TOKEN не установлена в настройках Railway!")
if not raw_channel_id:
    exit("Ошибка: Переменная CHANNEL_ID не установлена в настройках Railway!")

try:
    CHANNEL_ID = int(raw_channel_id)
except ValueError:
    exit("Ошибка: CHANNEL_ID должен быть числом (например, -100...)")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Напиши свой отзыв или предложение в чат, и я передам его администраторам канала."
    )

# 2. Обработчик для пересылки отзывов (текстовых сообщений)
@dp.message(F.text)
async def handle_review(message: types.Message):
    # Определяем, как подписать автора отзыва
    username = message.from_user.username
    user_info = f"@{username}" if username else f"{message.from_user.first_name} (ID: {message.from_user.id})"
    
    # Формируем текст сообщения для канала
    review_text = (
        f"📝 <b>Новый отзыв!</b>\n\n"
        f"👤 <b>От:</b> {user_info}\n"
        f"💬 <b>Текст:</b> {message.text}"
    )

    try:
        # Отправка сообщения в канал
        await bot.send_message(
            chat_id=CHANNEL_ID, 
            text=review_text, 
            parse_mode="HTML"
        )
        # Подтверждение пользователю
        await message.answer("✅ Спасибо! Твой отзыв успешно отправлен в канал.")
        logging.info(f"Отзыв от {user_info} успешно отправлен.")
        
    except Exception as e:
        # Если что-то пошло не так (например, бот не админ в канале)
        await message.answer("❌ Произошла ошибка при отправке. Попробуйте позже.")
        logging.error(f"Ошибка при отправке в канал: {e}")

# Главная функция запуска
async def main():
    logging.info("Бот запускается...")
    # Пропускаем накопившиеся сообщения, чтобы бот не спамил при включении
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную")
