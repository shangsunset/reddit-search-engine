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
        self.id_to_url = dict()
        self.doc_count = 0


    #assume that every document only has one unique url
    #parsed_text is a list of words
    def add_doc(self, url, parsed_text):
        self.doc_count += 1
        assert url not in self.id_to_url
        current_id = self.doc_count
        self.forward_index[current_id] = parsed_text
        self.id_to_url[current_id] = url

        for position, word in enumerate(parsed_text):
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append((position, current_id))



    def save_on_disk(self, index_dir):

        def dump_json_to_file(source, filename):
            file_path = os.path.join(index_dir, filename)
            f = open(file_path, "w")
            json.dump(source, f, indent=4)

        dump_json_to_file(self.forward_index, "forward_index")
        dump_json_to_file(self.inverted_index, "inverted_index")
        dump_json_to_file(self.id_to_url, "id_to_url")



class Searcher:

    def __init__(self, index_dir):
        self.forward_index = dict()
        self.inverted_index = dict()
        self.id_to_url = dict()


        def load_json_from_files(filename):
            file_path = os.path.join(index_dir, filename)
            return json.load(open(file_path))

        self.forward_index = load_json_from_files("forward_index")
        self.inverted_index = load_json_from_files("inverted_index")
        self.id_to_url = load_json_from_files("id_to_url")



    #query is a list of words: query -> [word1, word2, word3 ...]
    #find_doc returns all the documents coresponding to each word in query
    def find_doc(self, query):
        return sum([self.inverted_index[word] for word in query], [])


    def get_doc_url(self, doc_id):
        return self.id_to_url[doc_id]

def doc_to_index(crawled_files_dir, index_dir):
    indexer = Indexer()

    for filename in os.listdir(crawled_files_dir):
        opened_file = open(os.path.join(crawled_files_dir, filename))
        parsed_doc = parse_html(opened_file.read()).split(" ")

        indexer.add_doc(base64.b16decode(filename), parsed_doc)

    indexer.save_on_disk(index_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawled_files_dir', dest='crawled_files_dir', required=True)
    parser.add_argument('--index_dir', dest='index_dir', required=True)
    args = parser.parse_args()
    doc_to_index(args.crawled_files_dir, args.index_dir)


if __name__ == '__main__':
    main()
