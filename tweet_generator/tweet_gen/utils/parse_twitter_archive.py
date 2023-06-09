import zipfile
from json import JSONDecoder
import datetime
import pandas as pd
import logging


def extract_json_objects(text: str, decoder: JSONDecoder = JSONDecoder()):
    """
    Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    :param text: Source text containing JSON objects
    :param decoder: JSONDecoder
    :return: Generator with the json objects
    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1


def parse_archive(account_id: str, filename: str) -> str:
    """
    Extracts username and tweets from the archive file and saves the tweets as csv file

    :param account_id: User ID from relational database
    :param filename: File name of the archive
    :return: Username
    """
    logging.info("{} parsing twitter archive".format(account_id))
    archive = zipfile.ZipFile('files/archives/'+filename, 'r')
    account = extract_json_objects(archive.read('data/account.js').decode("utf-8"))
    username = next(account)["account"]["username"]
    _tweets = archive.read('data/tweet.js').decode("utf-8")

    tweets = []
    for tweet in extract_json_objects(_tweets):
        t = {
            "datetime": datetime.datetime.strptime(
                tweet['tweet']['created_at'], "%a %b %d %H:%M:%S %z %Y"
            ).strftime("%Y-%m-%d %H-%M-%S"),
            "hashtags": " ".join([tw["text"] for tw in tweet['tweet']['entities']["hashtags"]]),
            "mentions": " ".join([tw["name"] for tw in tweet['tweet']['entities']["user_mentions"]]),
            "links": " ".join([tw["url"] for tw in tweet['tweet']['entities']["urls"]]),
            "hashtags_length": len(tweet['tweet']['entities']["hashtags"]),
            "mentions_length": len(tweet['tweet']['entities']["user_mentions"]),
            "links_length": len(tweet['tweet']['entities']["urls"]),
            "tweet": tweet['tweet']['full_text']
        }
        tweets.append(t)

    tweets = pd.DataFrame(tweets)
    tweets.to_csv("files/dataset/{}.csv".format(account_id), index=False)
    logging.info("{} done parsing twitter archive".format(account_id))

    return username
