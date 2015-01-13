from utils import *
import logging
import os
import argparse
import base64
import json

logger = logging.getLogger(__name__)

#forward index:
#doc1 -> [how, to , learn, python]
#doc2 -> [what, is, python]

#inverted index:
#how -> [doc1]
#to -> [doc1]
#python -> [doc1, doc2]

class Indexer:
    def __init__(self):
        self.forward_index = dict()
        self.inverted_index = dict()
        self.url_to_id = dict()
        self.doc_count = 0


    #assume that every document only has one unique url
    #parsed_text is a list of words
    def add_doc(self, url, parsed_text):
        self.doc_count += 1
        assert url not in self.url_to_id
        current_id = self.doc_count
        self.forward_index[current_id] = parsed_text

        for position, word in enumerate(parsed_text):
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append((position, current_id))


    def save_on_disk(self, index_dir):
        forward_index_filename = os.path.join(index_dir, "forward_index")
        inverted_index_filename = os.path.join(index_dir, "inverted_index")
        url_to_id_filename = os.path.join(index_dir, "url_to_id")

        forward_index_file = open(forward_index_filename, "w")
        inverted_index_file = open(inverted_index_filename, "w")
        url_to_id_file = open(url_to_id_filename, "w")

        json.dump(self.forward_index, forward_index_file, indent=4)
        json.dump(self.inverted_index, inverted_index_file, indent=4)
        json.dump(self.url_to_id, url_to_id_file, indent=4)


def doc_to_index(crawled_files_dir, index_dir):
    indexer = Indexer()

    for filename in os.listdir(crawled_files_dir):
        opened_file = open(os.path.join(crawled_files_dir, filename))
        parsed_doc = parse_html(opened_file.read()).split(" ")

        indexer.add_doc(base64.b16decode(filename), parsed_doc)

    indexer.save_on_disk(index_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawled_files_dir', dest='crawled_files_dir')
    parser.add_argument('--index_dir', dest='index_dir')
    args = parser.parse_args()
    doc_to_index(args.crawled_files_dir, args.index_dir)


if __name__ == '__main__':
    main()
