FROM ubuntu:20.04

WORKDIR /cs_tweet_gen

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8002

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY requirements.txt /cs_tweet_gen/
RUN pip3 install -r requirements.txt

COPY . /cs_tweet_gen/
RUN python3 -m spacy download en_core_web_sm
RUN python3 setup.py
