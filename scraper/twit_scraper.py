from bs4 import BeautifulSoup
from urllib.request import urlopen
from xml.etree import ElementTree as etree
from db_scripts import twits as twits_db
import asyncio
import aiohttp
from urllib.error import HTTPError

'genadiy_g'
URL_MASK = "http://twitrss.me/twitter_user_to_rss/?user={}&fetch=Fetch+RSS"


async def get_twit(session, link, following_id):
    twit_id = link.split('/')[-1]

    async with session.get(link) as response:
        content = await response.content.read()
        soup = BeautifulSoup(content, "html.parser")
        twits_text = soup.find(class_='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text').text
        twits_text = twits_text.split('pic.twitter.com')[0] if 'pic.twitter.com' in twits_text else twits_text
        twit = twits_db.Twit(twit_id, following_id, twits_text)
    return twit


async def get_followings_twits(following_id):
    # user_name = user.user_id
    loop = asyncio.get_event_loop()

    url = URL_MASK.format(following_id)
    with urlopen(url, timeout=10) as r:
        items = etree.parse(r).find('channel').findall('item')

    links = [item.find('link').text for item in items]

    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [get_twit(session, link, following_id) for link in links]
        return await asyncio.gather(*tasks)


def check_following_exists(following_id):
    url = URL_MASK.format(following_id)
    try:
        urlopen(url, timeout=10)
        return True
    except HTTPError:
        return False


# loop = asyncio.get_event_loop()
# twits = loop.run_until_complete(get_followings_twits('genadiy_g'))
# print(twits)

# print(check_following_exists('genadiy_g'))

