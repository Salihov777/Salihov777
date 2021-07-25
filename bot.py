import logging
from aiogram import Bot, Dispatcher, executor, types
from ConfigPiton import ApiOWM, TokenTwo  # не забудь поменять токены
import aiogram.utils.markdown as fmt
import aiohttp
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Настроить ведение журнала
logging.basicConfig(level=logging.INFO)

# Инициализировать бота и диспетчера
bot = Bot(token=TokenTwo)  # не забудь поменять токены
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'старт'], commands_prefix='!/')
async def send_welcome(message: types.Message):
    """Этот обработчик будет вызываться, когда пользователь отправит команду `/ start` или` / help`  """
    await message.reply(f"Салам Алейкум  \n<b>{fmt.quote_html('Это твой бот-помощник в программировании')}</b>",
                        parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['help', 'помощь'])
async def send_welcome(message: types.Message):
    """Этот обработчик будет вызываться, когда пользователь отправит команду ` / help`  """
    await message.reply('Это бот могучего Python-разработчика')


@dp.message_handler(commands="specbuttons")
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию 🗺️", request_location=True,
                                      reply_markup=types.ReplyKeyboardRemove()))
    keyboard.add(types.KeyboardButton(text="Запросить контакт ☎️", request_contact=True,
                                      reply_markup=types.ReplyKeyboardRemove()))
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(commands="inline_url")
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Instagram", url="https://instagram.com"),
        types.InlineKeyboardButton(text="Оф. канал Telegram", url="https://t.me/rocknrolla_777")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Кнопки-ссылки", reply_markup=keyboard)


# ответ на отправку GIF пользователем
@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def echo_document(message: types.Message):
    await message.reply_animation(message.animation.file_id)


# Класс для FMS
class FindWeather(StatesGroup):
    city = State()
    drink = State()


# функция запроса
@dp.message_handler(commands='opros')
async def cmd_start(message: types.Message):
    await FindWeather.city.set()
    await message.answer("Введите название города, в котором хотите узнать погоду:")
#" пользователь пишет название города "


@dp.message_handler(state=FindWeather.city)
async def process_name(message: types.Message, state: FSMContext):
    city = message.text  # полученное название
    await message.answer(
        await get_weather(city)  # передаем в функцию
    )
    # Finish conversation
    await state.finish()


'''Вот функция , чтобы узнать погоду'''
async def get_weather(city):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        async with aiohttp.ClientSession() as session :
            params = {city: 'city', 'ApiOWM': ApiOWM}
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={ApiOWM}",params=params) as resp:
                dataInfo = await resp.json()


        data = dataInfo

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        return (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе: {city}\nТемпература: {cur_weather}°С {wd}\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                f"Продолжительность дня: {length_of_the_day}\n "
                f"***Хорошего дня!***"
                )
    except:
        return "\U00002620 Проверьте название города \U00002620"
'''  Конец истории с погодой '''


# Кнопки или buttons
'''пишу FSM про напитки '''
@dp.message_handler(commands=['drink'])
async def cmd_buttons_two(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # one_time_keyboard=True,
    buttons = ['with Sprite', 'with Coca-Cola', 'with Fanta']
    keyboard.add(*buttons)
    await message.answer("Выберите блюдо:", reply_markup=keyboard)
    await FindWeather.drink.set()
''' пользователь пишет название напиток '''


@dp.message_handler(state=FindWeather.drink)
async def process_name(message: types.Message, state: FSMContext):
    drink = message.text  # полученное название
    drink = drink.split(' ')[1]
    await message.answer(
        drink + ' ,спасибо за выбор'  , reply_markup=types.ReplyKeyboardRemove()
    )
    # Finish conversation
    await state.finish()


@dp.message_handler()
async def echo(message: types.Message):
    # обрабатывать все текстовые сообщения в чате
    await message.answer(message.text)


# Последний шаг: запустите длинный опрос.  '''
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
