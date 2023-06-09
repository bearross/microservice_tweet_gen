FROM ubuntu:20.04

WORKDIR /cs_tsoev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8006

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip

RUN apt-get install -y python3-flask
RUN apt-get install -y git

COPY requirements.txt /cs_tsoev/
RUN pip3 install -r requirements.txt

RUN pip3 install git+https://github.com/storerjeremy/python-semrush.git
RUN pip3 install git+https://github.com/NVIDIA/NeMo.git
RUN pip3 install bert-extractive-summarizer --upgrade --force-reinstall
RUN pip3 install git+https://github.com/boudinfl/pke.git
RUN pip3 install keybert

#RUN git clone https://github.com/seomoz/SEOmozAPISamples.git
#RUN python3 SEOmozAPISamples/python/setup.py install
#RUN pip3 install git+https://github.com/seomoz/SEOmozAPISamples.git#egg=mozscape&subdirectory=python
