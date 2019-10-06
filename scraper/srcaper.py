from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from xml.etree import ElementTree as etree

URL = "http://twitrss.me/twitter_user_to_rss/?user=genadiy_g&fetch=Fetch+RSS"

with urlopen(URL, timeout=10) as r:
    items = etree.parse(r).find('channel').findall('item')

links = [item.find('link').text for item in items]
print(links)


def get_twit(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    twits_text = soup.find(class_='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text').text
    twits_text = twits_text.split('pic.twitter.com')[0] if 'pic.twitter.com' in twits_text else twits_text
    print(twits_text)


get_twit(links[0])

for link in links:
    get_twit(link)
