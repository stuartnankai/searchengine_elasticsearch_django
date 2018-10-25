import os
import sys
import codecs
from elasticsearch import Elasticsearch, helpers
from bs4 import BeautifulSoup
import pandas as pd
import json


def process_text(text):
    text = text.strip().replace('\n', ' ')
    return ' '.join(text.split())


# dir_path = os.path.dirname(os.path.realpath(__file__))
#
es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

# es = Elasticsearch()
#
# for filename in os.listdir(os.path.join(dir_path, 'data')):
#     if filename.endswith('.html'):
#         print (filename)
#         file_path = os.path.join(dir_path, 'dataset/bbc/2018/10/1', filename)
#         article_id = filename.replace('.html', '')
#         url = 'http://www.jianshu.com/p/{0}'.format(article_id)
#         html_content = codecs.open(file_path, 'r', encoding='utf-8')
#         soup = BeautifulSoup(html_content, 'lxml')
#         title = soup.find('h1', class_='title').text
#         content = soup.find('div', class_='show-content').text
#         es.index(index='jianshu', doc_type='ariticle', id=article_id, body={
#             'url': url,
#             'title': process_text(title),
#             'content': process_text(content)
#         })

def docs_for_load():
    with open('/Users/jiansun/Documents/PyCharm/elasticsearch/elasticsearch/dataset/bbc/2018/10/1/articles') as f:
        reader = json.load(f)
        # helpers.bulk(es, reader, index='bbcnews', doc_type='article')
        for item in reader['articles']:
            yield {
                "_index": "bbcnews",
                "_type": "article",
                "doc": {
                    'title': item['title'],
                    'description': item['description'],
                    'section': item['section'],
                    'content': item['content'],
                    'link': item['link']
                },
                }
helpers.bulk(es, docs_for_load())


