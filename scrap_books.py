import pandas as pd
import requests
import re
import os
import sys

TAG_KNOWLEDGE_AREA = 'English Package Name'
TAG_URL = 'OpenURL'
TAG_NAME = 'Book Title'


def create_directory(name):

    if not os.path.exists(name):
        os.mkdir(name)
        print("Directory ", name, " Created ")
    else:
        print("Directory ", name, " already exists")


if __name__ == '__main__':

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', -1)

    try:
        saving_path = sys.argv[1]
    except IndexError:
        saving_path = "../springer_books/"
        create_directory(saving_path)

    reading_csv = pd.read_csv('books_springer.csv')
    # reading_csv = reading_csv[reading_csv[TAG_KNOWLEDGE_AREA] == "Computer Science"]

    # Create target Directory if doesn't exist
    areas = reading_csv[TAG_KNOWLEDGE_AREA].unique()
    for area in areas:
        create_directory(saving_path+"/"+area)

    pd_urls = reading_csv[[TAG_NAME, TAG_KNOWLEDGE_AREA, TAG_URL]]
    for i in range(0, len(pd_urls)):
        # iterate over rows
        row = pd_urls.iloc[i]
        print(row)
        # get the url from the response
        url_request = requests.get(row[TAG_URL])
        content_change = re.sub(r"book", "content/pdf", url_request.url)
        pdf_added = re.sub(r"$", r".pdf", content_change)
        with open(f'{saving_path}/{row[TAG_KNOWLEDGE_AREA]}/{re.sub(r"[^A-Za-z0-9]+", "", row[TAG_NAME])}.pdf', 'wb') as f:
            try:
                f.write(requests.get(pdf_added).content)
            except:
                print(f'{row[TAG_NAME]} from {row[TAG_KNOWLEDGE_AREA]} could not be downloaded')
            print("\n Done \n")














