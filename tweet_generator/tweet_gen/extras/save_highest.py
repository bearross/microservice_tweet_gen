import gzip
from os import walk
from os.path import join, basename, splitext
import pandas as pd
import re
import spacy
from spacy.matcher import Matcher
from save_dataset_standard import extract_username, data_files
nlp = spacy.load("en_core_web_sm")


for file_index in range(len(data_files)):
    print("working on: ", data_files[file_index])
    dataset = {}
    with gzip.open(data_files[file_index], 'rt') as f:
        print(data_files[file_index])
        intro = f.readline()
        print(intro)

        total_rows = int(intro.split(":")[1])
        total_rows = int((total_rows-1)/3)
        # total_rows = 1000000
        errors = 0
        for i in range(total_rows):
            try:
                line_time = f.readline().strip()
                line_user = f.readline().strip()
                username = extract_username(line_user[2:-1])
                line_post = f.readline().strip()
                _ = f.readline()

                if username in dataset.keys():
                    dataset[username] += 1
                else:
                    dataset[username] = 1
            except AttributeError:
                errors += 1

        print("errors: ", errors)

    df = pd.DataFrame()
    df['username'] = dataset.keys()
    df['tweets'] = dataset.values()
    # del dataset

    df = df.sort_values(by=['tweets'], ascending=False)
    df[df['tweets'] > 100].to_csv("files/stats/" + splitext(splitext(basename(data_files[file_index]))[0])[0] + ".csv", index=False)
