import asyncio
import logging
import random
from pathlib import Path
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from phrases import get_random_phrase

logging.basicConfig(level=logging.INFO)

TOKEN = "8324336218:AAFAfLhEZ1Jz5mmL7Qhwk7KN_1rfge6Pe3U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

MEMES_DIR = Path(__file__).parent / "memes"

# ID девушки
YOUR_CHAT_ID = 564525738

# -------------------------------------------------------------------
# Клавиатуры
# -------------------------------------------------------------------

def main_menu_keyboard():
    buttons = [
        [KeyboardButton(text="😊 Настроение")],
        [KeyboardButton(text="💐 Комплименты")],
        [KeyboardButton(text="🤗 Забота")],
        [KeyboardButton(text="💕 Нежность")],
        [KeyboardButton(text="📖 Наше")],
        [KeyboardButton(text="😄 Для улыбки")],
        [KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def mood_keyboard():
    buttons = [
        [KeyboardButton(text="😔 Грустно")],
        [KeyboardButton(text="😴 Устала")],
        [KeyboardButton(text="😤 Злишься")],
        [KeyboardButton(text="💔 Скучаю")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def compliments_keyboard():
    buttons = [
        [KeyboardButton(text="👀 Внешность")],
        [KeyboardButton(text="🧠 Характер")],
        [KeyboardButton(text="✨ Просто комплимент")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def care_keyboard():
    buttons = [
        [KeyboardButton(text="🌿 Забота")],
        [KeyboardButton(text="💡 Совет")],
        [KeyboardButton(text="💪 Мотивация")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def tenderness_keyboard():
    buttons = [
        [KeyboardButton(text="🥰 Ласковые")],
        [KeyboardButton(text="❤️ Любовь")],
        [KeyboardButton(text="🤗 Обнимашки")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def our_keyboard():
    buttons = [
        [KeyboardButton(text="💭 Воспоминания")],
        [KeyboardButton(text="📅 Планы")],
        [KeyboardButton(text="🤫 Секрет")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def fun_keyboard():
    buttons = [
        [KeyboardButton(text="😂 Шутка")],
        [KeyboardButton(text="🌟 Вдохновение")],
        [KeyboardButton(text="☀️ Доброе утро")],
        [KeyboardButton(text="🌙 Перед сном")],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# -------------------------------------------------------------------
# Ежедневные сообщения (только с 22 по 27 марта)
# -------------------------------------------------------------------

async def send_daily_messages():
    now = datetime.now()
    hour = now.hour
    day = now.weekday()
    month_day = now.day

    # Только с 22 по 27 марта
    if month_day < 22 or month_day > 27:
        return  # не отправляем ничего

    if hour == 9:
        await bot.send_message(YOUR_CHAT_ID, "Доброе утро, зайка моя! ☀️❤️ Улыбнись новому дню!")
    
    elif hour == 14:
        if day == 0:
            await bot.send_message(YOUR_CHAT_ID, "Как прошёл понедельник? Что делала? 🌸")
        elif day == 1:
            await bot.send_message(YOUR_CHAT_ID, "Как настроение? Поела сегодня вкусненького? 🍲")
        elif day == 2:
            await bot.send_message(YOUR_CHAT_ID, "Что нового? Чем занимаешься? 😊")
        elif day == 3:
            await bot.send_message(YOUR_CHAT_ID, "Как себя чувствуешь? Может, прилечь отдохнуть? 💤")
        elif day == 4:
            await bot.send_message(YOUR_CHAT_ID, "Пятница! Есть планы на вечер? 🎉")
        elif day == 5:
            await bot.send_message(YOUR_CHAT_ID, "Суббота! Как отдыхаешь? 🍃")
        elif day == 6:
            await bot.send_message(YOUR_CHAT_ID, "Воскресенье... Готовишься к новой неделе? 📝")
    
    elif hour == 22:
        await bot.send_message(YOUR_CHAT_ID, "Спокойной ночи, мой лучик! 😴🌙 Пусть тебе приснится что-то очень хорошее ❤️")

# -------------------------------------------------------------------
# Обработчики
# -------------------------------------------------------------------

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌟 Привет, моя хорошая!\n\n"
        "Это твоя личная книга любви и поддержки. Выбери раздел, и я подарю тебе тёплые слова.",
        reply_markup=main_menu_keyboard()
    )

@dp.message(F.text == "😂 Шутка")
async def send_random_meme(message: Message):
    if not MEMES_DIR.exists():
        await message.answer("📁 Папка с мемами не найдена. Попроси создать её.")
        return

    images = [f for f in MEMES_DIR.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]
    if not images:
        await message.answer("😢 Мемов пока нет, но скоро добавлю.")
        return

    random_meme = random.choice(images)
    with open(random_meme, 'rb') as meme:
        await message.answer_photo(meme, caption="😂 держи мем для настроения", reply_markup=fun_keyboard())

@dp.message(F.text == "😊 Настроение")
async def mood_section(message: Message):
    await message.answer("Что тебя беспокоит?", reply_markup=mood_keyboard())

@dp.message(F.text == "😔 Грустно")
async def sad_handler(message: Message):
    phrase = get_random_phrase("sad")
    await message.answer(phrase, reply_markup=mood_keyboard())

@dp.message(F.text == "😴 Устала")
async def tired_handler(message: Message):
    phrase = get_random_phrase("tired")
    await message.answer(phrase, reply_markup=mood_keyboard())

@dp.message(F.text == "😤 Злишься")
async def angry_handler(message: Message):
    phrase = get_random_phrase("angry")
    await message.answer(phrase, reply_markup=mood_keyboard())

@dp.message(F.text == "💔 Скучаю")
async def miss_handler(message: Message):
    phrase = get_random_phrase("miss")
    await message.answer(phrase, reply_markup=mood_keyboard())

@dp.message(F.text == "💐 Комплименты")
async def compliments_section(message: Message):
    await message.answer("Чем порадовать?", reply_markup=compliments_keyboard())

@dp.message(F.text == "👀 Внешность")
async def compliment_appearance_handler(message: Message):
    phrase = get_random_phrase("compliment_appearance")
    await message.answer(phrase, reply_markup=compliments_keyboard())

@dp.message(F.text == "🧠 Характер")
async def compliment_personality_handler(message: Message):
    phrase = get_random_phrase("compliment_personality")
    await message.answer(phrase, reply_markup=compliments_keyboard())

@dp.message(F.text == "✨ Просто комплимент")
async def compliment_general_handler(message: Message):
    phrase = get_random_phrase("compliment")
    await message.answer(phrase, reply_markup=compliments_keyboard())

@dp.message(F.text == "🤗 Забота")
async def care_section(message: Message):
    await message.answer("Что тебе нужно?", reply_markup=care_keyboard())

@dp.message(F.text == "🌿 Забота")
async def care_handler(message: Message):
    phrase = get_random_phrase("care")
    await message.answer(phrase, reply_markup=care_keyboard())

@dp.message(F.text == "💡 Совет")
async def advice_handler(message: Message):
    phrase = get_random_phrase("advice")
    await message.answer(phrase, reply_markup=care_keyboard())

@dp.message(F.text == "💪 Мотивация")
async def motivation_handler(message: Message):
    phrase = get_random_phrase("motivation")
    await message.answer(phrase, reply_markup=care_keyboard())

@dp.message(F.text == "💕 Нежность")
async def tenderness_section(message: Message):
    await message.answer("Выбирай:", reply_markup=tenderness_keyboard())

@dp.message(F.text == "🥰 Ласковые")
async def affection_handler(message: Message):
    phrase = get_random_phrase("affection")
    await message.answer(phrase, reply_markup=tenderness_keyboard())

@dp.message(F.text == "❤️ Любовь")
async def love_handler(message: Message):
    phrase = get_random_phrase("love")
    await message.answer(phrase, reply_markup=tenderness_keyboard())

@dp.message(F.text == "🤗 Обнимашки")
async def hug_handler(message: Message):
    phrase = get_random_phrase("hug")
    await message.answer(phrase, reply_markup=tenderness_keyboard())

@dp.message(F.text == "📖 Наше")
async def our_section(message: Message):
    await message.answer("Что вспомним или запланируем?", reply_markup=our_keyboard())

@dp.message(F.text == "💭 Воспоминания")
async def memory_handler(message: Message):
    phrase = get_random_phrase("memory")
    await message.answer(phrase, reply_markup=our_keyboard())

@dp.message(F.text == "📅 Планы")
async def plans_handler(message: Message):
    phrase = get_random_phrase("plans")
    await message.answer(phrase, reply_markup=our_keyboard())

@dp.message(F.text == "🤫 Секрет")
async def secret_handler(message: Message):
    phrase = get_random_phrase("secret")
    await message.answer(phrase, reply_markup=our_keyboard())

@dp.message(F.text == "😄 Для улыбки")
async def fun_section(message: Message):
    await message.answer("Что хочешь?", reply_markup=fun_keyboard())

@dp.message(F.text == "🌟 Вдохновение")
async def inspire_handler(message: Message):
    phrase = get_random_phrase("inspire")
    await message.answer(phrase, reply_markup=fun_keyboard())

@dp.message(F.text == "☀️ Доброе утро")
async def morning_handler(message: Message):
    phrase = get_random_phrase("morning")
    await message.answer(phrase, reply_markup=fun_keyboard())

@dp.message(F.text == "🌙 Перед сном")
async def evening_handler(message: Message):
    phrase = get_random_phrase("evening")
    await message.answer(phrase, reply_markup=fun_keyboard())

@dp.message(F.text == "🔙 Назад")
async def back_to_main(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())

@dp.message(F.text == "❓ Помощь")
async def help_handler(message: Message):
    help_text = (
        "📖 Как пользоваться книжкой любви:\n\n"
        "Выбери раздел, затем категорию — и я пришлю тёплое сообщение.\n"
        "Все фразы хранятся в моём сердечке и ждут именно тебя ❤️\n\n"
        "Если хочешь что-то изменить или добавить — напиши моему создателю."
    )
    await message.answer(help_text, reply_markup=main_menu_keyboard())

@dp.message()
async def unknown_message(message: Message):
    await message.answer(
        "Я понимаю только кнопки внизу экрана. Пожалуйста, выбери раздел.",
        reply_markup=main_menu_keyboard()
    )

# -------------------------------------------------------------------
# Запуск с планировщиком
# -------------------------------------------------------------------

scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_messages, 'cron', hour='9,14,22', minute=0)

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
