from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = "7255047394:AAHfdS_V4Hk5NyqF1M348fr0zvBomsRAtYg"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button, button2)
kb.row(button3)

catalog_kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
catalog_kb.row(button, button2, button3, button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)
    initiate_db()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# обработка состояния возрост
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# обработка состояния рост
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# обработка состояния вес и расчет колорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'ваша норма {result} колорий')
    await state.finish()


# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию
@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    results = get_all_product()
    for result in results:
        await message.answer(f'Название: {result[1]} | Описание: {result[2]} | Цена: {result[3]}')
        with open(f'{result[0]}.png', "rb") as photo:
            await bot.send_photo(message.from_user.id, photo)
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
