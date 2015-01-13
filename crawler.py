import time
from bs4 import BeautifulSoup
import logging
import os.path
import argparse
from base64 import b16encode
from utils import *

logger = logging.getLogger(__name__)

class Crawler:

    def __init__(self, url, file_dir):
        self.url = url
        self.file_dir = file_dir



    @staticmethod
    def _get_absolute_url(url):
        return "https://www.reddit.com" + url


    def crawl(self):
        current_page_url = self.url
        succeeded_url_count = 0
        failed_url_count = 0
        while True:

            if (succeeded_url_count + failed_url_count) % 100 == 0:
                logger.info("succeeded urls--{}, failed urls--{}".format(succeeded_url_count, failed_url_count))

            current_page = get_html(current_page_url)
            soup = BeautifulSoup(current_page)
            all_href_links = soup.find_all("a", attrs={"class": "title"})
            all_posts_links = [Crawler._get_absolute_url(link["href"]) for link in all_href_links]

            try:
                for i, post_link in enumerate(all_posts_links):
                    succeeded_url_count += 1
                    html = get_html(post_link)
                    filename = b16encode(post_link)
                    file_path = os.path.join(self.file_dir, filename)
                    stored_file = open(file_path, "w")
                    stored_file.write(html.encode('utf-8'))
                    stored_file.close()
                    time.sleep(2)

            except Exception as e:
                failed_url_count += 1
                logger.error('this is an error')
                logger.exception(e)

            next_page_url = soup.find("a", attrs={"rel": "next"})["href"]
            assert next_page_url is not None
            current_page_url = next_page_url
            time.sleep(2)

def main():

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')


    parser = argparse.ArgumentParser()
    parser.add_argument('--start_url', dest='url')
    parser.add_argument('--file_dir', dest='file_dir')
    args = parser.parse_args()
    crawler = Crawler(args.url, args.file_dir)
    crawler.crawl()


if __name__ == '__main__':
    main()
