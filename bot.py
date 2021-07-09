import logging
from aiogram import Bot, Dispatcher, executor, types
#import ConfigPiton
import aiogram.utils.markdown as fmt

# Configure logging               Настроить ведение журнала
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher   Инициализировать бота и диспетчера
bot = Bot(token='1797905957:AAGiG4ADxEhwRF7J5epQhTHCq6OPlcd2lYs')
dp = Dispatcher(bot)

# Кнопки или buttons

@dp.message_handler(commands=['buttons'])
async def cmd_buttons(message: types.Message):
    keydoard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width=2) #,input_field_placeholder)
    buttons =['with Sprite' , 'with Coca-Cola', 'with Fanta']
    keydoard.add(*buttons)
    await message.answer('what you drink ?', reply_markup=keydoard)

@dp.message_handler(commands=['start', 'старт'], commands_prefix='!/')
async def send_welcome(message: types.Message):
    '''Этот обработчик будет вызываться, когда пользователь отправит команду `/ start` или` / help`  '''
    await message.reply(f"Салам Алейкум  \n<b>{fmt.quote_html('Это твой бот-помощник в программировании')}</b>", parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands=['help', 'помощь'])
async def send_welcome(message: types.Message):
    '''Этот обработчик будет вызываться, когда пользователь отправит команду ` / help`  '''
    await message.reply('Это бот могучего Python-разработчика')

@dp.message_handler(commands=["specButtons"])
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
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

@dp.message_handler()
async def echo(message: types.Message):
    ''' обрабатывать все текстовые сообщения в чате'''
    if message.text == 'pogoda' :
        await message.reply('Вы запрашиваете погоду')
    if message.text == 'with Sprite' :
        await message.reply('Вы попросили Sprite!')
        await message.answer("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove()) #Чтобы удалить кнопки, необходимо отправить новое сообщение со специальной «удаляющей» клавиатурой типа ReplyKeyboardRemove
    else:
        await message.answer(message.text)


async def my_filter(message: types.Message):
    # do something here сделай что-нибудь здесь
    return {'foo': 'ВВедена новая команда', 'bar': 123987456}

@dp.message_handler(my_filter)
async def my_message_handler(message: types.Message, bar: int):
    await message.reply(f'bar = {bar}')

# ответ на отправку GIF пользователем
@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def echo_document(message: types.Message):
    await message.reply_animation(message.animation.file_id)


# новая фишка
@dp.message_handler(commands=['test4'])
async def with_hidden_link(message: types.Message):
    await message.answer(
        f"{fmt.hide_link('https://telegram.org/')}Кто бы мог подумать, что "
        f"в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
        f"возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
        f"когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
        f"коронавируса, команда Павла Дурова не растерялась и сделала качественные "
        f"видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)",
        parse_mode=types.ParseMode.HTML)
#не сработало ((
''' в эхо-боте эта функция отдельно похоже не работает
@dp.message_handler(lambda message: message.text == 'with Sprite')
async def without_puree(message: types.Message):
    await message.reply("Вы попросили Sprite!")
'''
@dp.message_handler(commands=["special_buttons"])
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Выберите действие:", reply_markup=keyboard)





#Последний шаг: запустите длинный опрос.  '''
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



