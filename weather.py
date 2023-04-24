import requests
import os


def get_temperature(city: str) -> float:
	"""
	Функция осуществляет запрос к API OpenWeatherMap
	и получает информацию о погоде в указанном городе.
	"""
	api_key = os.getenv('WEATHERTOKEN')
	url = 'https://api.openweathermap.org/data/2.5/weather'
	params = {'q': city, 'units': 'metric', 'appid': api_key}
	response = requests.get(url, params=params)


	if response.status_code == 200:
		try:
			weather_data = response.json()
			temp = weather_data['main']['temp']
			humidity = weather_data['main']['humidity']
			wind_speed = weather_data['wind']['speed']

			weather_info = f"Сейчас в городе {city}:\nтемпература {temp} градусов Цельсия, " \
					   f"влажность {humidity}%, скорость ветра {wind_speed} м/с."

			return (weather_info)
		except KeyError as e:
			return f"Ошибка при обработке данных: {e}"
	elif response.status_code == 404:
		return f"Город {city} не найден"
	else:
		return f"Ошибка при запросе к API: {response.text}"





