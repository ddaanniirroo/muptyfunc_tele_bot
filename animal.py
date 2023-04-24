import requests
import os


def get_random_cute_animal_photo_url():
	"""
	Функция обращается к API Unsplash
	и получает случайное фото с милыми животными.
	"""
	access_key = os.getenv("UNPLASHTOKEN")
	url = 'https://api.unsplash.com/photos/random?query=cute%20animals'
	headers = {'Authorization': f'Client-ID {access_key}'}

	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		data = response.json()
		photo_url = data['urls']['regular']
		return photo_url
	else:
		return f'Request failed with status code {response.status_code}'

