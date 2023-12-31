import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6982492984:AAHEBeSovlkPki02WIxrFvYI4-i_BwLK_cU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# клавиатура
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("Список команд"))
menu.add(KeyboardButton("Меню"))
menu.add(KeyboardButton("Где нас найти?"))


# список гео кофеен
locations = [
    {"title": "Кофейня 1", "address": "Арбатская", "apartment": "21"},
    {"title": "Кофейня 2", "address": "Краснопресненская набережная", "apartment": "21"},
]

# генерация клавиатуры с инлайн-кнопками для гео
locations_keyboard = InlineKeyboardMarkup()
for location in locations:
    locations_keyboard.add(
        InlineKeyboardButton(text=location["title"], callback_data=f"location:{location['address']}:{location['apartment']}"))


# обработка команды
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет! Я бот кофейни: my coffee, чтобы воспользоваться мной, выбери команды ниже.", reply_markup=menu)


# команда /help обработка
@dp.message_handler(lambda message: message.text == "Список команд", content_types=types.ContentTypes.TEXT)
async def process_help_command(message: types.Message):
    await message.answer("Список команд:\n/start - начать работу с ботом\n/help - список команд\n/menu - посмотреть меню", reply_markup=menu)


# команда /menu обработка
@dp.message_handler(lambda message: message.text == "Меню", content_types=types.ContentTypes.TEXT)
async def process_menu_command(message: types.Message):
    await message.answer("Меню с ценами:\n1. Эспрессо - €2\n2. Латте - €2.5\n3. Капучино - €2\n4. РАФ Карамельный - €4.5\n5. Круасан - €1.25\n6. Донат в ассортименте - €1.5pcs", reply_markup=menu)


# кнопка "Где нас найти?"
@dp.message_handler(lambda message: message.text == "Где нас найти?", content_types=types.ContentTypes.TEXT)
async def process_location_button(message: types.Message):
    await message.answer("Выбери кофейню, чтобы увидеть её местоположение:", reply_markup=locations_keyboard)


# кнопки с гео
@dp.callback_query_handler(lambda c: c.data.startswith('location'))
async def process_location_button(callback_query: types.CallbackQuery):
    _, address, apartment = callback_query.data.split(":")
    location_text = f"Вы выбрали кофейню :\n{address} {apartment}"
    await bot.send_message(callback_query.from_user.id, location_text)


# запуск
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)