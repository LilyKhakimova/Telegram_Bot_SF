import telebot
from config import TOKEN, values, menu_list, help_list
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    bot.send_message(message.chat.id, menu_list)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Здравствуйте! Этот бот поможет Вам с конвертацией валют. Для просмотра доступных команд введите ‘/menu’")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, help_list)


@bot.message_handler(commands=['values'])
def values_message(message):
    bot.send_message(message.chat.id, 'Доступные валюты:')
    for i in values:
        bot.send_message(message.chat.id, i + ' ' + values[i])


@bot.message_handler(content_types=['text'])
def convert_result(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) != 3:
            raise APIException('Неверно введены данные')

        base, quote, amount = val
        result = CryptoConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f'{amount} {values[base]} в {values[quote]} равно: {result}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
