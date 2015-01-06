import requests
from bs4 import BeautifulSoup
import re

_learnprogramming_pattern = re.compile("https://(www.)?reddit.com/r/learnprogramming/")

def get_html(page_url):
    assert _learnprogramming_pattern.match(page_url)
    headers = {"User-Agent": "reddit search engine version 0.1 by shangsunset"}
    r = requests.get(page_url, headers=headers)
    if r.status_code != 200:
        raise Exception("invalid status code, {}".format(r.status_code))

    return r.text

def parse_html(html_code):
    soup = BeautifulSoup(html_code)
    return soup.select("div.usertext-body")[1].text
