from db_scripts import user as user_db
from tg_bot.bot import bot


if __name__ == '__main__':
    user_db.create_table()
    bot.polling()
