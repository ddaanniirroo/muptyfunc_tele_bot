from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import os

import weather, exchange, animal

class WeatherDialog(StatesGroup):
	city = State()

class ExchangeDialog(StatesGroup):
	iso = State()
	amount = State()

class MyForm(StatesGroup):
	question = State()
	options = State()


class MyBot:
	def __init__(self, token) -> None:
		self.api = Bot(token)
		self.dp = Dispatcher(self.api, storage=MemoryStorage())


	async def start_command(self, message: types.Message):
		"""
		Данная функция предоставляет пользователю возможность выбора функций,
		которые доступны в боте.
		Она создает клавиатуру с несколькими кнопками,
		каждая из которых соответствует определенной функции,
		"""
		markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
		weather = KeyboardButton("Погода")
		exchange = KeyboardButton("Конвертировать валюту")
		animal = KeyboardButton("Милое животное")
		create_pool = KeyboardButton("Создать опрос")
		markup.add(weather, exchange, animal, create_pool)

		await message.reply("Привет, выберите функцию", reply_markup=markup)



	async def router(self, message: types.Message):
		"""
		Данная функция отвечает за маршрутизацию пользовательских запросов и определение,
		какую функцию бота нужно вызвать в зависимости от полученного сообщения.
		Внутри функции используется объект ReplyKeyboardMarkup,
		который создает клавиатуру с возможными командами бота.
		"""
		if message.text == "Погода":
			await message.answer("В каком городе интересует погода?")
			await WeatherDialog.city.set()
		if message.text == "Конвертировать валюту":
			await message.answer("Код валюты, которую вы хотите приобрести?")
			await ExchangeDialog.iso.set()
		if message.text == "Милое животное":
			photo_url = animal.get_random_cute_animal_photo_url()
			await message.answer_photo(photo_url)
		if message.text == "Создать опрос":
			await message.answer("Введите вопрос для опроса:")
			await MyForm.question.set()



	async def process_city(self, message: types.Message, state: FSMContext):
		"""
		Данная функция предназначена для получения актуальной погоды в заданном городе
		"""
		async with state.proxy() as data:
			data['city'] = message.text
		city = data['city']
		data = weather.get_temperature(city)
		await message.answer(data)
		await state.finish()


	async def process_currency(self, message: types.Message, state: FSMContext):
		"""
		Мы получаем код ISO от пользователя,
		запрашиваем у него необходимую информацию
		и обновляем текущее состояние на основе этой информации.
		Так же мы вызываем функцию проверки кода iso
		"""
		async with state.proxy() as data:
			data['iso'] = message.text.upper()  # переводим код валюты в верхний регистр
		iso = data['iso']
		error_message = exchange.check_currency_code(iso)
		if error_message:
			await message.answer(error_message)
			await state.finish()
		else:
			await message.answer(f"Введите количество USD для конвертации в {iso}:")
			await ExchangeDialog.next()


	async def process_amount(self, message: types.Message, state: FSMContext):
		"""
		Эта функция отправляет запрос к API,
		получает ответ по курсу валют и возвращает его пользователю.
		"""
		async with state.proxy() as data:
			data['amount'] = message.text
			iso = data['iso']
			amount = float(data['amount'])
		data = exchange.usd_to_currency(iso)
		converted_amount = round(amount * data, 2)
		await message.answer(f"{amount} USD = {converted_amount} {iso}")
		await state.finish()


	async def process_question(self, message: types.Message, state: FSMContext):
		"""
		Получаем от пользователя вопрос для опроса
		и обновляем текущее состояние в соответствии с введенными данными.
		"""
		async with state.proxy() as data:
			data['question'] = message.text

		await message.answer("Введите варианты ответов через запятую:")

		await MyForm.options.set()


	async def process_options(self, message: types.Message, state: FSMContext):
		"""
		Эта функция получает от пользователя варианты ответов для создания опроса,
		формирует опрос и отправляет его в чат.
		"""
		async with state.proxy() as data:
			data['options'] = message.text.split(',')

		question = data['question']
		group_chat_id = os.getenv('CHATID')
		await self.api.send_poll( group_chat_id, question, data["options"], is_anonymous=False)

		await state.finish()


	async def handle_all_other_messages(self, message: types.Message):
		"""
		Эта функция обрабатывает сообщение от пользователя,
		которое не связано с какими-либо конкретными функциями бота,
		и отправляет инструкцию по работе с ним. Таким образом,
		пользователь может получить помощь и указания по использованию бота.
		"""
		await message.answer("Простите, я не понимаю Вас. Выберите одну из доступных команд или функций. /start - для открытия меню")

