import requests
import telebot

url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = ''
api_telegram = ''

bot = telebot.TeleBot(api_telegram)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('welcome.png', 'rb')
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.username) + ',' + '\n' +
	 'Напиши мне название твоего города а я тебе информацию о погоде в твоем городе!')


@bot.message_handler(content_types=['text'])
def weather_send(message):
	s_city = message.text
	try:
		params = {'APPID': api_weather, 'q': s_city, 'units': 'metric'}
		result = requests.get(url, params=params)
		weather = result.json()

		bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(float(weather["main"]['temp'])) + "\n" + 
				"Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" + 
				"Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" + 
				"Скорость ветра " + str(float(weather['wind']['speed'])) + "\n" + 
				"Давление " + str(float(weather['main']['pressure'])) + "\n" + 
				"Влажность " + str(float(weather['main']['humidity'])) + "\n" + 
				"Видимость " + str(weather['visibility']) + "\n" + 
				"Описание " + str(weather['weather'][0]["description"]) + "\n")

		if weather["main"]['temp'] < 10:
			bot.send_message(message.chat.id, "Сейчас холодно!")
		elif weather["main"]['temp'] < 20:
			bot.send_message(message.chat.id, "Сейчас прохладно!")
		elif weather["main"]['temp'] > 38:
			bot.send_message(message.chat.id, "Сейчас жарко!")
		else:
			bot.send_message(message.chat.id, "Сейчас отличная температура!")

	except:
		bot.send_message(message.chat.id, "Город " + s_city + " не найден")


if __name__ == '__main__':
	bot.polling(none_stop=True)
