from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from xml.etree import ElementTree as etree


'genadiy_g'
URL_MASK = "http://twitrss.me/twitter_user_to_rss/?user={}&fetch=Fetch+RSS"


def get_twit(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    twits_text = soup.find(class_='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text').text
    twits_text = twits_text.split('pic.twitter.com')[0] if 'pic.twitter.com' in twits_text else twits_text
    return twits_text


def get_user_twits(user_name):
    url = URL_MASK.format(user_name)
    with urlopen(url, timeout=10) as r:
        items = etree.parse(r).find('channel').findall('item')

    links = [item.find('link').text for item in items]

    twits = []
    for link in links:
        twit = get_twit(link)
        twits.append(twit)
    return twits


twits = get_user_twits('genadiy_g')
print(twits)
