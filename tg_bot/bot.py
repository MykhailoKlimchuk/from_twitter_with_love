import telebot
from db_scripts import user as user_db
from db_scripts import following as following_db


with open('configs/token') as token_file:
    TOKEN = token_file.read()


def subscribe(message):
    user, session = user_db.get_user(message.from_user.id)
    user.wants_to_subscribe = True
    user.wants_to_unsubscribe = False
    session.commit()

    bot.send_message(message.chat.id, 'Напиши ид юзера на кого хочешь подписаться пример @genadiy_g')


def unsubscribe(message):
    user, session = user_db.get_user(message.from_user.id)
    user.wants_to_subscribe = False
    user.wants_to_unsubscribe = True
    session.commit()

    bot.send_message(message.chat.id, 'Напиши ид юзера от кого хочешь отписаться пример @genadiy_g')


COMMANDS = {
    'Добавить подписку': subscribe,
    'Отказаться от подписки': unsubscribe,
}

bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row(*COMMANDS.keys())


@bot.message_handler(commands=['start'])
def start_message(message):
    user, session = user_db.get_user(message.from_user.id)
    response_message = f'Привет, {message.from_user.first_name} я буду пересылать тебе твиты твоих подписок'

    bot.send_message(message.chat.id, response_message, reply_markup=keyboard1)
    session.commit()


@bot.message_handler(content_types=['text'])
def button_click(message):
    button_cb = COMMANDS.get(message.text, None)
    user, session = user_db.get_user(message.from_user.id)

    if button_cb is not None:
        button_cb(message)
        return

    if user.get_subscribe_status is not None:
        response_message = resolve_followings_id(user, message.text, session)
        bot.send_message(message.chat.id, response_message, reply_markup=keyboard1)

    session.commit()


def resolve_followings_id(user, following_id, session):
    response_message = ''
    if user.get_subscribe_status() is True:
        following_db.add_following(following_id, user.user_id, session)
    else:
        following_db.del_following(following_id, user.user_id, session)
    return response_message

