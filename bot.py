import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

BOT_TOKEN = "7526638876:AAGG1SF7VJP995VkqKkKD0F7sqIkii56Ooo"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------------------------- #
# Головне меню
# ---------------------------- #
def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📘 Про MathMento")
    kb.button(text="🧠 Пройти тест")
    kb.button(text="💬 Питання (FAQ)")
    kb.button(text="📅 Записатись на урок")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# ---------------------------- #
# Старт
# ---------------------------- #
@dp.message(Command("start"))
async def start_cmd(message: Message):
    try:
        photo = FSInputFile("start.png")
        caption = (
            f"👋 <b>Привіт, {message.from_user.first_name}!</b>\n\n"
            "Я — 🤖 <b>MathMentoBot</b> — твій помічник з математики!\n\n"
            "📘 Обери дію нижче 👇"
        )
        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML", reply_markup=main_menu())
    except Exception:
        await message.answer("⚠️ Файл start.jpg не знайдено. Додай його в папку з bot.py.", reply_markup=main_menu())

# ---------------------------- #
# Про MathMento
# ---------------------------- #
@dp.message(F.text == "📘 Про MathMento")
async def about(message: Message):
    try:
        photo = FSInputFile("ава.jpg")
        caption = (
            "<b>📗 MathMento</b> — онлайн-школа підготовки до <b>НМТ</b> та шкільної математики.\n\n"
            "✅ Індивідуальні заняття\n"
            "✅ Онлайн через Zoom / Meet\n"
            "✅ Практика на реальних тестах\n"
            "✅ Підтримка 24/7 💬\n\n"
            "📅 Запишись на безкоштовний пробний урок 👇"
        )

        kb = InlineKeyboardBuilder()
        kb.button(text="📅 Записатись на урок", url="https://mathmento.github.io/mathmento2/#contacts")
        kb.button(text="🌐 Відвідати сайт", url="https://mathmento.github.io/mathmento2/")
        kb.button(text="📸 Instagram", url="https://www.instagram.com/nmt_math._/")
        kb.adjust(1)

        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML", reply_markup=kb.as_markup())
    except Exception:
        await message.answer("⚠️ Не знайдено файл 'ава.jpg'.")

# ---------------------------- #
# Міні-тест
# ---------------------------- #
user_steps = {}
user_correct = {}
user_tasks = {}

TASKS = [
    ("2 + 3", 5),
    ("7 - 4", 3),
    ("5 × 6", 30),
    ("9 ÷ 3", 3),
    ("4²", 16),
    ("10 - 7 + 2", 5),
    ("3 × (2 + 1)", 9),
    ("15 ÷ 5", 3),
    ("8 + 12", 20),
    ("7 × 3 - 2", 19),
]

def get_random_tasks():
    return random.sample(TASKS, 3)

@dp.message(F.text == "🧠 Пройти тест")
async def start_test(message: Message):
    user_id = message.from_user.id
    tasks = get_random_tasks()
    user_tasks[user_id] = tasks
    user_steps[user_id] = 0
    user_correct[user_id] = 0

    first_example = tasks[0][0]
    await message.answer(f"🧩 Почнемо тест із 3 запитань!\n\n1️⃣ Обчисли: {first_example} = ?")

@dp.message(F.text.regexp(r"^-?\d+$"))
async def handle_answer(message: Message):
    user_id = message.from_user.id
    step = user_steps.get(user_id, 0)
    correct = user_correct.get(user_id, 0)
    tasks = user_tasks.get(user_id, [])

    if not tasks:
        return

    try:
        ans = int(message.text)
    except ValueError:
        await message.answer("Введи число 🔢")
        return

    if ans == tasks[step][1]:
        correct += 1

    step += 1
    user_steps[user_id] = step
    user_correct[user_id] = correct

    if step < 3:
        next_example = tasks[step][0]
        await message.answer(f"{step + 1}️⃣ Обчисли: {next_example} = ?")
    else:
        emoji, comment = (
            ("🌟", "Блискуче! Ти справжній математик!") if correct == 3 else
            ("🙂", "Добре! Ще трохи практики!") if correct == 2 else
            ("🤔", "Спробуй ще раз 💪")
        )

        kb = InlineKeyboardBuilder()
        kb.button(text="🔁 Пройти ще раз", callback_data="retry_test")
        kb.button(text="📅 Записатись на урок", url="https://mathmento.github.io/mathmento2/#contacts")
        await message.answer(
            f"{emoji} <b>Твій результат:</b> {correct}/3 правильних!\n\n{comment}",
            parse_mode="HTML",
            reply_markup=kb.as_markup()
        )
        user_steps[user_id] = 0

@dp.callback_query(F.data == "retry_test")
async def retry(callback: CallbackQuery):
    user_id = callback.from_user.id
    tasks = get_random_tasks()
    user_tasks[user_id] = tasks
    user_steps[user_id] = 0
    user_correct[user_id] = 0
    first_example = tasks[0][0]
    await callback.message.answer(f"🧩 Почнемо спочатку!\n\n1️⃣ Обчисли: {first_example} = ?")
    await callback.answer()

# ---------------------------- #
# Питання (FAQ)
# ---------------------------- #
@dp.message(F.text == "💬 Питання (FAQ)")
async def faq(message: Message):
    text = (
        "❓ <b>Часті питання:</b>\n\n"
        "📘 <b>Як проходять заняття?</b>\nОнлайн через Zoom або Google Meet.\n\n"
        "⏰ <b>Скільки триває урок?</b>\n60 хвилин.\n\n"
        "🎯 <b>Чи готуєте до НМТ?</b>\nТак! Повна програма з теорією, практикою та тестами.\n\n"
        "💸 <b>Чи є пробний урок?</b>\nТак, абсолютно безкоштовний!\n\n"
        "📅 Натисни «Записатись на урок», щоб почати 👇"
    )
    await message.answer(text, parse_mode="HTML")

# ---------------------------- #
# Записатись на урок
# ---------------------------- #
@dp.message(F.text == "📅 Записатись на урок")
async def signup(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🔗 Відкрити сайт", url="https://mathmento.github.io/mathmento2/#contacts")
    await message.answer("🗓 Обери зручний час 👇", reply_markup=kb.as_markup())

# ---------------------------- #
# Запуск
# ---------------------------- #
async def main():
    print("✅ MathMentoBot запущено! Чекаю натискання кнопок…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
