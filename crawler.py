import time
from bs4 import BeautifulSoup
import logging
import os.path
import argparse
from utils import *





class Crawler:

    def __init__(self, url, file_dir):
        self.url = url
        self.file_dir = file_dir



    @staticmethod
    def _get_absolute_url(url):
        return "https://www.reddit.com" + url


    def crawl(self):
        current_page_url = self.url
        while True:
            current_page = get_html(current_page_url)
            soup = BeautifulSoup(current_page)
            all_href_links = soup.find_all("a", attrs={"class": "title"})
            all_posts_links = [Crawler._get_absolute_url(link["href"]) for link in all_href_links]
            # logging.debug(all_posts_links)

            for i, post_link in enumerate(all_posts_links):
                text = parse_html(get_html(post_link))
                filename = "page" + str(i) + ".txt"
                file_path = os.path.join(self.file_dir, filename)
                stored_file = open(file_path, "w")
                stored_file.write(text)
                time.sleep(2)


            next_page_url = soup.find("a", attrs={"rel": "next"})["href"]
            current_page_url = next_page_url
            time.sleep(2)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_url', dest='url')
    parser.add_argument('--file_dir', dest='file_dir')
    args = parser.parse_args()
    crawler = Crawler(args.url, args.file_dir)
    crawler.crawl()


if __name__ == '__main__':
    main()
