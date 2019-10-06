from bs4 import BeautifulSoup
from urllib.request import urlopen
from xml.etree import ElementTree as etree
import asyncio
import aiohttp

'genadiy_g'
URL_MASK = "http://twitrss.me/twitter_user_to_rss/?user={}&fetch=Fetch+RSS"


async def get_twit(session, link):
    async with session.get(link) as response:
        content = await response.content.read()
        soup = BeautifulSoup(content, "html.parser")
        twits_text = soup.find(class_='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text').text
        twits_text = twits_text.split('pic.twitter.com')[0] if 'pic.twitter.com' in twits_text else twits_text
    return twits_text


async def get_user_twits(user_name):
    loop = asyncio.get_event_loop()

    url = URL_MASK.format(user_name)
    with urlopen(url, timeout=10) as r:
        items = etree.parse(r).find('channel').findall('item')

    links = [item.find('link').text for item in items]

    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [get_twit(session, link) for link in links]
        return await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
twits = loop.run_until_complete(get_user_twits('genadiy_g'))
print(twits)
