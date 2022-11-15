import telebot
import extensions
from config import token

telebot.apihelper.ENABLE_MIDDLEWARE = True


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
	bot.send_message(message.from_user.id, "Здравствуйте! Для рассчёта стоимости валют, введите в одном сообщении:\n"
										   "<Имя валюты, цену которой хотите узнать> <Имя валюты, в которой нужно узнать цену> <Количество первой валюты>\n"
										   "Список доступных команд: \n"
										   "/help или /start - вывод этого сообщения \n"
										   "/values - вывести список доступных валют \n"
										   )


@bot.message_handler(commands=['values'])
def values(message):
	bot.send_message(message.from_user.id, "Список доступных валют: \n"
										   "USD, RUB, EUR")


@bot.message_handler(func=lambda message: True)
def get_text_messages(message):
	print(message.text)
	user_request = message.text.rsplit()
	if len(user_request) != 3:
		answer = 'Пожалуйста, введите запрос в формате <первая валюта> <вторая валюта> <количество первой валюты>'
		print(answer)
		bot.send_message(message.from_user.id, answer)
	else:
		base = user_request[0].upper()
		quote = user_request[1].upper()
		try:
			amount = abs(float(user_request[2]))
		except ValueError:
			answer = 'Число должно быть десятичной дробью с точкой в качестве разделителя'
			bot.send_message(message.from_user.id, answer)
			raise extensions.APIException(answer)
		if base == quote:
			answer = 'Валюты должны отличаться'
			bot.send_message(message.from_user.id, answer)
			raise extensions.APIException(answer)
		if base not in ['USD', 'RUB', 'EUR'] or quote not in ['USD', 'RUB', 'EUR']:
			answer = 'Одна из валют указана неверно'
			bot.send_message(message.from_user.id, answer)
			raise extensions.APIException(answer)
		else:
			result = extensions.MoneyExchange().get_price(base, quote, amount)
			answer = f'Стоимость {amount} {base} - {result} {quote}'
			print(answer)
			bot.send_message(message.from_user.id, answer)


bot.infinity_polling(none_stop=True, interval=1)


