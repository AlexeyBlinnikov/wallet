from email import message
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from excel import append_values
from datetime import datetime
from aiogram.dispatcher.filters import Text
# from start import TOKEN, bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# TOKEN = "6743689178:AAHt0ePvr3SPh3nHWn63eqZJKucoKmiv6BE"
TOKEN = '5524654123:AAHfHmtyG1-s1G0JtZFbQX7FInrgh9fo50g'


storage = MemoryStorage()

bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    price = State()
    top = State()
    top_month = State()


xr = []

start_kb = ReplyKeyboardMarkup().add(KeyboardButton("🔝Приход💰")).add(KeyboardButton("❌Расход📉"))#.add(KeyboardButton("📝Анализ🧮"))
earn_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Аренда", callback_data='button1')).add(InlineKeyboardButton('Продажа', callback_data='button2')).insert(InlineKeyboardButton('Парикмахерская', callback_data='button3')).add(InlineKeyboardButton('Банк', callback_data='button4')).insert(InlineKeyboardButton('Спорт_оборудование', callback_data='button5'))
spend_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Аренда", callback_data='button_spend_1')).add(InlineKeyboardButton('Товарка', callback_data='button_spend_2')).insert(InlineKeyboardButton('Повседневные', callback_data='button_spend_3')).add(InlineKeyboardButton('Парикмахерская', callback_data='button_spend_4')).insert(InlineKeyboardButton('Спорт_оборудование', callback_data='button_spend_5'))


async def on_startup(_):
	print('Бот вышел в онлайн!')
async def on_shutdown(_):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    print(f'Произошла ошибка!\nДата:{current_date}\nВремя: {current_time}')
# spend_rent_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Go Pro", callback_data='spend_rent_1')).add(InlineKeyboardButton('Пылесос', callback_data='spend_rent_2'))
# @dp.register_message_handler(text = "🔝Приход💰")
async def start(message: types.Message):
        await bot.send_message(message.from_user.id, "Привет", reply_markup=start_kb)

async def top_up(message: types.Message):
        await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=earn_kb)
async def spend(message: types.Message):
        await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=spend_kb)
# async def analysis(message: types.Message):
#         await bot.send_message(message.from_user.id, "Выбери дату", reply_markup=start_kb)




# Приход инлайн ответ на кэлбэки первого уровня
# ------------------------------------Приход денег, вывод новых кнопок---------------------------------
async def topup_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup = InlineKeyboardMarkup()
                            .add(InlineKeyboardButton('Пылесос', callback_data = 'top_up_vacuumcleaner'))
							.insert(InlineKeyboardButton('Ps5', callback_data = 'top_up_ps'))
                            .add(InlineKeyboardButton('Тепловизор', callback_data = 'top_up_teplovisor'))
                            .insert(InlineKeyboardButton('Go pro', callback_data = 'top_up_gopro'))
                            .add(InlineKeyboardButton('Пароочиститель', callback_data = 'top_up_sc4'))
                            .insert(InlineKeyboardButton('Мойщик окон', callback_data = 'top_up_robot')))
    await callback_query.answer()

async def topup_callback_button3(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup = InlineKeyboardMarkup()
                            .add(InlineKeyboardButton('Прошлый месяц', callback_data = 'top_up_hairdresser_last'))
							.add(InlineKeyboardButton('Этот месяц', callback_data = 'top_up_hairdresser_now')))
    await callback_query.answer()

async def topup_callback_button5(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup = InlineKeyboardMarkup()
                            .add(InlineKeyboardButton('Эхолот', callback_data = 'top_up_eholot')))
    await callback_query.answer()

async def topup_callback_button2(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup = InlineKeyboardMarkup()
                            .add(InlineKeyboardButton('Ведро 6л', callback_data = 'top_up_6litr'))
							.add(InlineKeyboardButton('Ведро 8л', callback_data = 'top_up_8litr')))
    await callback_query.answer()

# ------------------------------------Приход денег, ввод данных в гугл таблицы---------------------------------
async def topup_callback_button2_6l(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Ведро 6 литров")
    await bot.send_message(callback_query.from_user.id, "Введи выручку от ведра 6л")
    await callback_query.answer()
async def topup_callback_button2_8l(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Ведро 8 литров")
    await bot.send_message(callback_query.from_user.id, "Введи выручку от ведра 8л")
    await callback_query.answer()
async def topup_callback_button4(callback_query: types.CallbackQuery):
    await Form.top_month.set()
    xr.insert(0, "Банк")
    await bot.send_message(callback_query.from_user.id, "Введи сумму за прошлый месяц")
    await callback_query.answer()

async def top_up_vacuumcleaner(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Пылесос")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_playstation(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "PlayStation")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_teplovisor(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Тепловизор")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_gopro(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Го про")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_sc4(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Пароочиститель")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_robot(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Мойщик окон")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()

async def top_up_hairdresser_last(callback_query: types.CallbackQuery):
    await Form.top_month.set()
    xr.insert(0, "Парикмахерская")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_hairdresser_now(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Парикмахерская")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()
async def top_up_eholot(callback_query: types.CallbackQuery):
    await Form.top.set()
    xr.insert(0, "Эхолот")
    await bot.send_message(callback_query.from_user.id, "Введи сумму")
    await callback_query.answer()



# -----------------------------------------------------
# Трата инлайн ответ на кэлбэки ПЕРВОГО уровня
async def spend_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Вложения в:", reply_markup = InlineKeyboardMarkup()
                            .add(InlineKeyboardButton('Плойка', callback_data = 'spend_ps5'))
                            .insert(InlineKeyboardButton('Пылесос', callback_data = 'spend_vacuum'))
                            .add(InlineKeyboardButton('Go pro', callback_data = 'spend_gopro'))
                            .insert(InlineKeyboardButton('Пароочиститель', callback_data = 'spend_sc4'))
                            # .add(InlineKeyboardButton('Go pro', callback_data = 'spend_gopro'))
							.add(InlineKeyboardButton('Тепловизор', callback_data = 'spend_teplovisor')))
                            # .add(InlineKeyboardButton('Робот мойщик окон', callback_data = 'spend_robot')))
    await callback_query.answer()

async def spend_callback_button2(callback_query: types.CallbackQuery):#, state: FSMContext):
    await Form.price.set()
    xr.insert(0, "Товар")
    await bot.send_message(callback_query.from_user.id, "Расходы на товарку")
    await callback_query.answer()

async def spend_callback_button3(callback_query: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Повседневные")
    await bot.send_message(callback_query.from_user.id, "Повседневные расходы за сегодня:")
    await callback_query.answer()

async def spend_callback_button4(callback_query: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Парикмахерская")
    await bot.send_message(callback_query.from_user.id, "Парикмахерская расходы:")
    await callback_query.answer()

async def spend_callback_button5(callback_query: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Аренда сибирка")
    await bot.send_message(callback_query.from_user.id, "Потратил на арендные товары для сибирки:")
    await callback_query.answer()

# Трата инлайн ответ на кэлбэки ВТОРОГО уровня
async def spend_rent_gopro(callback_query: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Го про")
    await bot.send_message(callback_query.from_user.id, "Потратил на го про сегодня:")
    await callback_query.answer()
async def spend_rent_vacuum(callback_query: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Пылесос")
    await bot.send_message(callback_query.from_user.id, "Потратил на пылесос сегодня:")
    await callback_query.answer()
async def spend_rent_ps5(call: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "PlayStation")
    await call.message.answer("Потратил на PlayStation сегодня")
    await call.answer()
async def spend_rent_sc4(call: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Пароочиститель")
    await call.message.answer("Потратил на Пароочиститель сегодня")
    await call.answer()
async def spend_rent_teplovisor(call: types.CallbackQuery):
    await Form.price.set()
    xr.insert(0, "Тепловизор")
    await call.message.answer("Потратил на Тепловизор сегодня")
    await call.answer()

# ___________________________________________
# трата
async def load_spend(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    current_date = datetime.now().date()
    append_values("B4:D4", current_date, f"{xr[0]}", f"{data['price']}")
    await bot.send_message(message.from_user.id, f"Добавлены траты на {xr[0]} в размере: {data['price']}", reply_markup=start_kb)
    await state.finish()

# пополнение
async def load_up(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    current_date = datetime.now().date()
    append_values("F4:H4", current_date, f"{xr[0]}", f"{data['price']}")
    await bot.send_message(message.from_user.id, f"Доходы от {xr[0]} в размере: {data['price']} добавлены", reply_markup=start_kb)
    await state.finish()


# Доделать пополнение за прошлый месяц
async def load_up_last(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    now = datetime.now()
    last_month = now.month-1 if now.month > 1 else 12
    year = now.year - 1 if last_month == 12 else now.year
    # last_year = now.year - 1
    append_values("F4:H4", f"{year}-{last_month}-01", f"{xr[0]}", f"{data['price']}")
    await bot.send_message(message.from_user.id, f"Доходы за прошлый месяц от {xr[0]} в размере: {data['price']} добавлены", reply_markup=start_kb)
    await state.finish()


# Отмена ввода
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return 
    await state.finish()
    await message.reply('Ввод отменен')

try:
    def register_handlers_client(dp : Dispatcher):
        dp.register_message_handler(start, commands=['start'])
        dp.register_message_handler(top_up, Text(equals = '🔝Приход💰'))
        dp.register_message_handler(spend, Text(equals = '❌Расход📉'))
        # dp.register_message_handler(analysis, Text(equals ='📝Анализ🧮'))
        # dp.register_message_handler(top_up, commands=['start'])

        dp.register_callback_query_handler(topup_callback_button1, Text(equals = 'button1'))
        dp.register_callback_query_handler(topup_callback_button2, Text(equals = 'button2'))
        dp.register_callback_query_handler(topup_callback_button3, Text(equals = 'button3'))
        dp.register_callback_query_handler(topup_callback_button4, Text(equals = 'button4'))
        dp.register_callback_query_handler(topup_callback_button5, Text(equals = 'button5'))
        dp.register_callback_query_handler(spend_callback_button1, Text(equals = 'button_spend_1'))
        dp.register_callback_query_handler(spend_callback_button2, Text(equals = 'button_spend_2'))#, state = None)
        dp.register_callback_query_handler(spend_callback_button3, Text(equals = 'button_spend_3'))
        dp.register_callback_query_handler(spend_callback_button4, Text(equals = 'button_spend_4'))
        dp.register_callback_query_handler(spend_callback_button5, Text(equals = 'button_spend_5'))
        dp.register_callback_query_handler(top_up_vacuumcleaner, Text(equals = 'top_up_vacuumcleaner'))
        dp.register_callback_query_handler(top_up_gopro, Text(equals = 'top_up_gopro'))
        dp.register_callback_query_handler(top_up_robot, Text(equals = 'top_up_robot'))
        dp.register_callback_query_handler(top_up_teplovisor, Text(equals = 'top_up_teplovisor'))
        dp.register_callback_query_handler(top_up_sc4, Text(equals = 'top_up_sc4'))
        dp.register_callback_query_handler(top_up_playstation, Text(equals = 'top_up_ps'))
        dp.register_callback_query_handler(topup_callback_button2_6l, Text(equals = 'top_up_6litr'))
        dp.register_callback_query_handler(topup_callback_button2_8l, Text(equals = 'top_up_8litr'))
        dp.register_callback_query_handler(top_up_hairdresser_last, Text(equals = 'top_up_hairdresser_last'))
        dp.register_callback_query_handler(top_up_hairdresser_now, Text(equals = 'top_up_hairdresser_now'))
        dp.register_callback_query_handler(top_up_eholot, Text(equals = 'top_up_eholot'))
        dp.register_callback_query_handler(spend_rent_gopro, Text(equals = 'spend_gopro'))
        dp.register_callback_query_handler(spend_rent_vacuum, Text(equals = 'spend_vacuum'))
        dp.register_callback_query_handler(spend_rent_ps5, Text(equals = 'spend_ps5'))
        dp.register_callback_query_handler(spend_rent_sc4, Text(equals = 'spend_sc4'))
        dp.register_callback_query_handler(spend_rent_teplovisor, Text(equals = 'spend_teplovisor'))
        
        # dp.register_callback_query_handler(spend_rent_robot, Text(equals = 'spend_robot'))

        # dp.register_callback_query_handler(load_spend, state = Form.info)
        dp.register_message_handler(cancel, state = "*", commands = ['отмена'])
        dp.register_message_handler(load_spend, state = Form.price)
        dp.register_message_handler(load_up, state = Form.top)
        dp.register_message_handler(load_up_last, state = Form.top_month)
        # dp.register_message_handler(cancel, state = "*", commands = ['отмена'])
        # dp.register_message_handler(cancel, Text(equals='отмена', ignore_case= True), state = "*")

except Exception as Ex:
    print(f"Возникла ошибка 1 {Ex} !!!!!!!!!")


try:
    register_handlers_client(dp)
except Exception as Ex:
    print(f"Возникла ошибка 2 {Ex}!!!!!!!!!")



try:
    executor.start_polling(dp, skip_updates = True, on_startup=on_startup, on_shutdown=on_shutdown)
except Exception as Ex:
    print(f"Возникла ошибка 3 {Ex} !!!!!!!!!")
