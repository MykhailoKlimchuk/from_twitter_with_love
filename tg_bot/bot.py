import telebot
from db_scripts import user as user_db
from db_scripts import following as following_db
from scraper.twit_scraper import check_following_exists


with open('configs/token') as token_file:
    TOKEN = token_file.read()


def subscribe(message):
    user, session = user_db.get_user(message.from_user.id, message.chat.id)
    user.wants_to_subscribe = True
    user.wants_to_unsubscribe = False
    session.commit()

    bot.send_message(message.chat.id, 'Напиши ид юзера на кого хочешь подписаться пример @genadiy_g')


def unsubscribe(message):
    user, session = user_db.get_user(message.from_user.id, message.chat.id)
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
    user, session = user_db.get_user(message.from_user.id, message.chat.id)
    response_message = f'Привет, {message.from_user.first_name} я буду пересылать тебе твиты твоих подписок'

    bot.send_message(message.chat.id, response_message, reply_markup=keyboard1)
    session.commit()


@bot.message_handler(content_types=['text'])
def button_click(message):
    button_cb = COMMANDS.get(message.text, None)
    user, session = user_db.get_user(message.from_user.id, message.chat.id)

    if button_cb is not None:
        button_cb(message)
        return

    if user.get_subscribe_status is not None:
        response_message = resolve_followings_id(user, message.text, session)
        bot.send_message(message.chat.id, response_message, reply_markup=keyboard1)

    session.commit()


def resolve_followings_id(user, following_id, session):
    following_id = following_id[1:]

    if user.get_subscribe_status() is True:
        if check_following_exists(following_id) is False:
            response_message = f'Я не нашел в твиттере пользователя {following_id}'
        else:
            following_db.add_following(following_id, user.user_id, session)
            response_message = f'Вы подписались на {following_id}'
    else:
        if following_db.del_following( following_id, user.user_id, session) is True:
            response_message = f'Вы отписались от {following_id}'
        else:
            response_message = f'{following_id} нету в ваших подписках'

    return response_message
