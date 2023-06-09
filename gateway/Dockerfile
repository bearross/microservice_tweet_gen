FROM ubuntu:20.04

WORKDIR /cs_gateway

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY requirements.txt /cs_gateway/
RUN pip3 install -r requirements.txt

COPY . /cs_gateway/
