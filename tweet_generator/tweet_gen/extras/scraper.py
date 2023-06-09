import scrapy
import spacy
from tweet_gen.utils.collect_texts import get_paragraphs

nlp = spacy.load("en_core_web_sm")


class Spider(scrapy.Spider):
    name = 'Wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/Electric_battery']

    def parse(self, response):
        # texts = nltk.clean_html(response)
        item = dict()
        item['url'] = response.url
        # item['title'] = response.meta['link_text']
        # extracting basic body
        para = "\n".join(response.xpath('//body//text()').extract())
        doc = nlp(para)
        para = list(doc.sents)
        para = get_paragraphs(nlp, para)

        item['body'] = para
        print(item)
