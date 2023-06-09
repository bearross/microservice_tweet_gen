import gzip
from os import walk
from os.path import join
import pandas as pd
import re
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
hashtags_pattern = [{'ORTH': '#'}, {'IS_ASCII': True}]
mentions_pattern = [{'TEXT': {"REGEX": r'(@)\w+'}}]
links_pattern = [{'LIKE_URL': True}]
USERNAME = "sadidul012"


def extract_username(url):
    return re.search(r'http://twitter.com/([^/?]+)', url).group(1)


def process_row(row):
    doc = nlp(row["tweet"])
    matcher = Matcher(nlp.vocab)
    matcher.add("HashTags", [hashtags_pattern])
    matcher.add("Mentions", [mentions_pattern])
    matcher.add("URLs", [links_pattern])
    matches = matcher(doc)

    hashtags = []
    mentions = []
    links = []
    for match_id, start, end in matches:
        element = doc[start:end].text

        if element[0] == "@":
            mentions.append(element)
        elif element[0] == "#":
            hashtags.append(element)
        else:
            links.append(element)

    row["length"] = len(doc)
    row["hashtags"] = "\n".join(hashtags)
    row["mentions"] = "\n".join(mentions)
    row["links"] = "\n".join(links)
    row["hashtags_length"] = len(hashtags)
    row["mentions_length"] = len(mentions)
    row["links_length"] = len(links)
    if row.name != 0 and row.name % 10000 == 0:
        print("done processing", row.name)
    return row


dataset_location = "/media/sadid/Speed/tweets/"

data_files = []
for root, dirs, files in walk(dataset_location, topdown=False):
    for file in files:
        data_files.append(join(root, file))

# file_index = 6

if __name__ == '__main__':
    dataset = []

    for file_index in range(len(data_files)):
        print("\n\nworking on: ", data_files[file_index])
        with gzip.open(data_files[file_index], 'rt') as f:
            intro = f.readline()
            print(intro, end="")

            total_rows = int(intro.split(":")[1])
            total_rows = int((total_rows - 1) / 3)
            # total_rows = 100000
            errors = 0
            founds = 0
            for i in range(total_rows):
                line_time = f.readline().strip()
                line_user = f.readline().strip()
                line_post = f.readline().strip()
                _ = f.readline()

                try:
                    username = extract_username(line_user[2:-1])
                    if username == USERNAME:
                        dataset.append({
                            "datetime": line_time[2:-1],
                            "username": username,
                            "tweet": line_post[2:-1]
                        })
                        founds += 1
                except AttributeError:
                    errors += 1

            print("founds:", founds)
            print("errors:", errors)

    dataset = pd.DataFrame(dataset)
    dataset = dataset.apply(lambda x: process_row(x), axis=1)
    dataset.to_csv("files/dataset/" + USERNAME + ".csv", index=False)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(dataset.sample(10)[["tweet", "length", "mentions", "mentions_length", "hashtags", "hashtags_length", "links", "links_length"]])
