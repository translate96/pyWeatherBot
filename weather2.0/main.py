import requests
import telebot


url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = ''
api_telegram = ''

bot = telebot.TeleBot(api_telegram)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',' + '\n' +
	 'я бот погода.')



@bot.message_handler(content_types=['text'])
def weather_send(message):
	s_city = message.text


	try:

		params = {'APPID': api_weather, 'q': s_city, 'units': 'metric', 'lang': 'ru'}
		result = requests.get(url, params=params)
		weather = result.json()

		three_d = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={'q': s_city, 
			'appid': api_weather, 'units': 'metric', 'lang': 'ru', 'cnt': '4'}).json()

		array = [str(i['dt_txt']) + " " + str(i['weather'][0]['description']) + " " + str(i['main']['temp']) for i in three_d['list']]
		three_days = ('\n'.join(map(str, array)))

		if weather["main"]['temp'] < 10:
			state = "Сейчас холодно!"
		elif weather["main"]['temp'] < 20:
			state = "Сейчас прохладно!"
		elif weather["main"]['temp'] > 38:
			state = "Сейчас жарко!"
		else:
			state = "Сейчас отличная температура!"

		bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(float(weather["main"]['temp'])) + "\n" +
				"Скорость ветра " + str(float(weather['wind']['speed'])) + "\n" + 
				"Давление " + str(float(weather['main']['pressure'])) + "\n" + 
				"Влажность " + str(float(weather['main']['humidity'])) + "\n" + 
				"Видимость " + str(weather['visibility']) + "\n" + 
				"Описание " + str(weather['weather'][0]["description"]) + 
				"\n" + state + "\n\n" + three_days)

	except:
		bot.send_message(message.chat.id, "Город " + s_city + " не найден")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(1)
            print(e)
