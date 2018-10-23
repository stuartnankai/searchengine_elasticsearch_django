from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from elasticsearch import Elasticsearch


def index(request):
    keywords = request.GET.get('keywords', '').strip()
    if keywords == '':
        return render(request, 'searchengine/index.html', {
            'title': 'BBC NEWS SEARCH',
            'keywords': keywords,
            'err_info': '',
            'result': [],
        })
    else:
        result = get_elastic_search_result(keywords)
        if len(result) == 0:
            return render(request, 'searchengine/index.html', {
                'title': 'BBC NEWS SEARCH',
                'keywords': keywords,
                'err_info': 'NO CONTENTS',
                'result': [],
            })
        else:
            return render(request, 'searchengine/index.html', {
                'title': 'BBC NEWS SEARCH',
                'keywords': keywords,
                'err_info': 'TOP 5 NEWS',
                'result': result,
            })


def get_elastic_search_result(keywords):
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    result = es.search(index='bbcnews', doc_type='article', body={
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {"doc.content": keywords}
                    },
                    {
                        "match": {"doc.content": keywords}
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "title": {},
                "content": {}
            }
        },
        "from": 0,
        "size": 5
    })
    # print("This is lenght")
    # print(len(result))
    # # for i in result:
    # #     print("This is result:", i)
    # #     print("++++++++++++++++++++++++++++++++++")
    # print("This is total:")
    # print(result['hits']['total'])
    #
    # print("This is max_scoure:")
    # print(result['hits']['max_score'])
    #
    # # print("This is hits:")
    # # print(result['hits']['hits'])
    #
    #
    # for j in result['hits']['hits']:
    #     print(j['_source']['doc']['title'])

    # print("This is hits hits")
    # print(result['hits']['hits'])
    #
    print("This is item")
    for item in result['hits']['hits']:
        print(item)

    return [{
        'url': item['_source']['doc']['link'],
        'title': item['_source']['doc']['title'],
        'description': item['_source']['doc']['description'],
        'section': item['_source']['doc']['section'],
        'content': item['_source']['doc']['content']
    } for item in result['hits']['hits']]






    # return [{'url': item['_source']['url'],
    #          'title': mark_safe(' '.join(item['highlight']['title'])),
    #          'content': mark_safe(' '.join(item['highlight']['content']))}
    #         for item in result['hits']['hits']]