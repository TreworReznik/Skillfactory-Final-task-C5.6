import telebot
from extensions import CryptoConverter, APIException
from database import keys, BOT

bot = telebot.TeleBot(BOT)

@bot.message_handler(commands=['start', 'help'])
def start(message:telebot.types.Message):
    text = f'Привет {message.chat.first_name}\n'\
'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты>  \
<в какую валюту перевести > \
<количество перводимой валюты>\nСписок всех доступных валют ---> /values \nЦена доллара в рублях  ---> /usd_rub \
\nЦена евро в рублях ---> /eur_rub \
\nЦена юаня в рублях ---> /cny_rub'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['usd_rub'])
def usd_rub(message):
    text = CryptoConverter.get_price('доллар', 'рубль', '1')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['eur_rub'])
def eur_rub(message):
    text = CryptoConverter.get_price('евро', 'рубль', '1')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['cny_rub'])
def cny_rub(message):
    text = CryptoConverter.get_price('юань', 'рубль', '1')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message:telebot.types.Message):

    try:
        values = message.text.lower().split(' ')

        if len(values) != 3 :
            raise APIException("Слишком много параметров.")

        quote, base, amount = values
        total = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} - {total}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)