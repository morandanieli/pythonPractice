
import json
import difflib
import os
import requests
from urllib.parse import urlparse


def fetch_dictionary_data(download_link):
    parsed_url = urlparse(download_link)
    local_file_path = parsed_url.path.replace("/", "") + '-' + parsed_url.query
    if not os.path.isfile(local_file_path):
        response = requests.get(download_link)
        with open(local_file_path, "wb") as f:
            f.write(response.content)

    f = open(local_file_path, "r")
    return json.load(f)


def translate(dictionary_data):
    keys = dictionary_data.keys()

    while True:
        search_term = input("Please enter your search term: ")
        if search_term in keys:
            print("Dictionary meaning: ")
            meaning = dictionary_data[search_term]
            for i,m in enumerate(meaning):
                print("({})".format(i+1), m)
        else:
            close_matches = difflib.get_close_matches(search_term, keys, n=3, cutoff=0.3)
            if close_matches:
                print("Term not found, possible close terms:")
                for i,o in enumerate(close_matches):
                    print("({}) ".format(i+1), o)
            else:
                print("Term not found")


if __name__ == '__main__':
    download_link = 'https://drive.google.com/uc?export=download&id=1WvcRzSnpusMM0AkVN_NpUDsc6rdL9_Uf'
    dict_data = fetch_dictionary_data(download_link)
    translate(dict_data)


