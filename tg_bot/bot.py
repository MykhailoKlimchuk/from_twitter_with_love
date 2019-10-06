import telebot
from db_scripts import user as user_db

with open('configs/token') as token_file:
    TOKEN = token_file.read()


def subscribe(message):
    user = user_db.get_user(message.from_user.id)
    user.subscribe()
    bot.send_message(message.chat.id, 'Напиши ид юзера на кого хочешь подписаться пример @genadiy_g')


def unsubscribe(message):
    user = user_db.get_user(message.from_user.id)
    user.unsubscribe()
    bot.send_message(message.chat.id, 'Напиши ид юзера от кого хочешь отписаться пример @genadiy_g')


COMMANDS = {
    'Подписаться': subscribe,
    'Отписаться': unsubscribe,
}

bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row(*COMMANDS.keys())


@bot.message_handler(commands=['start'])
def start_message(message):
    user = user_db.get_user(message.from_user.id)
    response_message = f'Привет, {message.from_user.first_name} я буду пересылать тебе твиты твоих подписок'

    bot.send_message(message.chat.id, response_message, reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def button_click(message):
    button_cb = COMMANDS.get(message.text, None)
    user = user_db.get_user(message.from_user.id)

    if button_cb is not None:
        button_cb(message)
        return

    if user.get_subscribe_status is not None:
        user.process_subscribe_data(message.text)



bot.polling()
