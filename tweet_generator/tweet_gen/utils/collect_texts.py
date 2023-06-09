import pandas as pd
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
import spacy
import logging
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests


__nlp = spacy.load("en_core_web_sm")


def tag_visible(element):
    """
    Finds elements with texts

    :param element: BeautifulSoup element
    :return: Boolean
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_paragraphs(_nlp: spacy.Language, _text: list) -> list:
    """
    Finds paragraphs from raw texts

    :param _nlp: Language for finding paragraph
    :param _text: List of strings
    :return: List of paragraphs
    """
    p = []
    word_count = 0
    for index, sent in enumerate(_text):
        if len(sent) > 5:
            sentence_doc = _nlp(sent)
            w_c = len(sentence_doc)
            if word_count + w_c > 510:
                break

            word_count += w_c
            if sentence_doc.vector_norm < 3.0:
                p.append(re.sub(r'\s+', ' ', sentence_doc.text))

    return p


def extract_keywords(_nlp: spacy.Language, sequence: str, special_tags: list = None) -> list:
    """
    Extract keywords from string/tweet

    :param _nlp: Language for finding keywords
    :param sequence: Source string/tweet
    :param special_tags: Accepted spacy tags lists
    :return: List for keywords
    """
    result = []
    pos_tag = ['PROPN', 'NOUN', 'ADJ']

    doc = _nlp(sequence.lower())

    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)

    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if token.pos_ in pos_tag and not token.like_url:
                final_chunk = final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())

    return list(set(result))


def collect_text_url(url: str) -> str:
    """
    Collect paragraph from URL.

    :param url: Source url
    :return: Paragraph
    """
    f = requests.get(url)
    soup = BeautifulSoup(f.text, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    text = [t.strip() for t in visible_texts]
    para = " ".join(get_paragraphs(__nlp, text))

    return para


def collect_text_wiki(page_id: str) -> str:
    """
    Collect summary from wikipedia

    :param page_id: Wikipedia page id/page title
    :return: Summary from wikipedia
    """
    text = None
    try:
        text = wikipedia.summary(page_id)
    except (PageError, DisambiguationError) as e:
        pass

    return text


def _collect_text_with_tweet(tweet: str) -> [str, int]:
    """
    Collects summary from wikipedia using keyword from the tweet

    :param tweet: Tweet
    :return: Summary text and number of wiki link visited
    """
    text = None
    keywords = extract_keywords(__nlp, tweet)
    wiki_results = []
    for keyword in keywords:
        results = wikipedia.search(keyword)
        wiki_results.extend(results)

    i = 0

    while i < len(wiki_results):
        text = collect_text_wiki(wiki_results[i])
        if text is not None:
            return text, i
        i += 1

    return text, i


def collect_texts(user_id: int):
    """
    Collects texts for a user and save into the dataset
    :param user_id: User ID from relational database
    """
    logging.info("{} collecting texts...".format(user_id))
    file_name = "files/dataset/{}.csv".format(user_id)

    dataset = pd.read_csv(file_name)
    total = dataset.shape[0]
    texts = []
    error = 0
    for index, row in dataset.iterrows():
        text, i = _collect_text_with_tweet(row["tweet"])
        error += 1 if text is None else 0
        if index % 3 == 0:
            logging.info("{} {}/{} collection error {}".format(user_id, index, total, error))
        texts.append(text)

    logging.info("{} done collecting texts...".format(user_id))
    logging.info("{} saving dataframe...".format(user_id))

    logging.info(dataset.shape, len(texts))
    dataset["texts"] = texts
    dataset.to_csv(file_name, index=False)

    logging.info("{} done saving dataframe...".format(user_id))
