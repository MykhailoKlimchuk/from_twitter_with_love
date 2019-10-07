from db_scripts import user as user_db
from db_scripts import following as following_db
from db_scripts import twits as twits_db
from tg_bot.bot import bot
from scraper import twit_scraper
import asyncio
import aiohttp


def get_all_users_twits():
    all_users = user_db.get_all_users()
    users_following_dict = {}

    for user in all_users:
        users_following_dict[user.user_id] = following_db.get_user_followings(user.user_id)
    # todo: получить для каждого юзера его подписки
    # todo: для кажой подписки получить список новых твитов
    # todo: отправить на публикацию


if __name__ == '__main__':
    # get_all_users_twits()
    user_db.create_table()
    following_db.create_table()
    twits_db.create_table()
    bot.polling()
