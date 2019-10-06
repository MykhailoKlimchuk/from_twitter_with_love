import telebot


with open('configs/token') as token_file:
    TOKEN = token_file.read()


def subscribe(message):
    bot.send_message(message.chat.id, 'Напиши ид юзера на кого хочешь подписаться пример @genadiy_g')


def unsubscribe(message):
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
    bot.send_message(message.chat.id, 'Привет, я буду пересылать тебе твиты твоих подписок', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def button_click(message):
    button_cb = COMMANDS.get(message.text, None)
    if button_cb is None:
        return

    button_cb(message)
