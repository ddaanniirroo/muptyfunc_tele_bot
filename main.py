from aiogram.utils import executor
import tele_bot as tb
from dotenv import load_dotenv
import os

if __name__ == '__main__':
	load_dotenv()
	teletoken = os.getenv('TELETOKEN')
	bot = tb.MyBot(teletoken)
	bot.dp.message_handler(commands=['start'])(bot.start_command)
	bot.dp.message_handler(lambda message: message.text in ["Погода", "Конвертировать валюту",
						      "Милое животное", "Создать опрос"], state=None)(bot.router)
	bot.dp.message_handler(state=tb.WeatherDialog.city)(bot.process_city)
	bot.dp.message_handler(state=tb.ExchangeDialog.iso)(bot.process_currency)
	bot.dp.message_handler(state=tb.ExchangeDialog.amount)(bot.process_amount)
	bot.dp.message_handler(state=tb.MyForm.question)(bot.process_question)
	bot.dp.message_handler(state=tb.MyForm.options)(bot.process_options)
	bot.dp.message_handler()(bot.handle_all_other_messages)
	executor.start_polling(bot.dp, skip_updates=True)
