import requests
import os



def usd_to_currency(currency_code: str):
	"""
	Функция обращается к Exchange Rate API,
	чтобы получить актуальный курс валюты.
	"""
	API_KEY = os.getenv('EXCHANGETOKEN')
	BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
	response = requests.get(BASE_URL)
	if response.status_code == 200:
		data = response.json()
		if currency_code not in data['conversion_rates']:
			return -1
		usd_to_currency = data['conversion_rates'][currency_code]
		return usd_to_currency
	else:
		return f'Request failed with status code {response.status_code}'


def check_currency_code(iso):
	"""
	Функция проверяет,
	является ли введенный код ISO действительным,
	и сообщает об ошибке, если код не существует
	"""
	API_KEY = os.getenv('EXCHANGETOKEN')
	BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
	try:
		response = requests.get(BASE_URL)
		data = response.json()
		if iso.upper() not in data['conversion_rates']:
			return f"Неправильный код валюты: {iso}"
	except:
		return "Ошибка при запросе к API"

