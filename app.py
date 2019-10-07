from db_scripts import user as user_db
from db_scripts import following as following_db
from db_scripts import twits as twits_db
from tg_bot.bot import bot
from scraper import twit_scraper
import asyncio
import aiohttp


async def get_user_twits(user):
    followings = following_db.get_user_followings(user.user_id)
    tasks = [twit_scraper.get_followings_twits(following.following_id) for following in followings]
    return await asyncio.gather(*tasks)


async def get_all_users_twits():
    all_users = user_db.get_all_users()
    tasks = [get_user_twits(user) for user in all_users]
    return await asyncio.gather(*tasks)


def publish_twit(chat_id, twit_text, following_id):
    text = f'''
{following_id} twitted:
{twit_text}
    '''
    bot.send_message(chat_id, text)


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def publish_twits(twits):
    for twit in twits:
        followings = following_db.get_following_by_following_id(twit.following_id)
        for following in followings:
            user = user_db.get_user(following.user_id)[0]
            publish_twit(user.chat_id, twit.twit_text, following.following_id)


if __name__ == '__main__':
    # get_all_users_twits()
    user_db.create_table()
    following_db.create_table()
    twits_db.create_table()

    loop = asyncio.get_event_loop()
    twits = loop.run_until_complete(get_all_users_twits())
    twits = flatten(twits)
    print(twits)
    publish_twits(twits)

    bot.polling()
