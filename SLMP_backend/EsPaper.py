import json
from flask import Flask, request
from elasticsearch import Elasticsearch
import requests
import arxiv


ES = Elasticsearch("https://xx.xx.xx.2:8920", basic_auth=('elastic',
                   'WxHj21=d6jyMMEHM+M=-'), ca_certs=False, verify_certs=False)
INDEX_NAME = "papers"


#
# print(result)


app = Flask(__name__)


@app.route('/page')
def paperPage():
    current = request.args.get('current')
    size = request.args.get('size')
    keyword = request.args.get('keyword')
    if keyword == '':
        query = {
            "query": {
                "match_all": {}
            },
            'from': current,
            'size': size
        }
    else:
        query = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"title": keyword}},
                        {"match": {"abstract": keyword}}
                    ]
                }
            },
            'from': current,
            'size': size
        }
    result = ES.search(index=INDEX_NAME, body=query)
    return result.body['hits']


@app.route('/complete')
def autoComplete():
    keyword = request.args.get('keyword')
    query = {
        "suggest": {
            "blog-suggest": {
                "prefix": keyword,
                "completion": {
                    "size": "10",
                    "field": "title.simple",
                    "skip_duplicates": True,
                    "fuzzy": {
                        "fuzziness": 0
                    }
                }
            }
        }
    }
    result = ES.search(index=INDEX_NAME, body=query)
    hits = result.body['suggest']['blog-suggest'][0]['options']
    titles = [{"title": h['text'], "id":h['_id']} for h in hits]
    return {'data': titles}


@app.route('/pageMore')
def pareMore():
    current = request.args.get('current')
    size = request.args.get('size')
    title = request.args.get('title')
    author = request.args.get('author')
    abstract = request.args.get('abstract')
    query = {
        "query": {
            "bool": {
                "must": []
            }
        },
        'from': current,
        'size': size
    }

    if title:
        query["query"]["bool"]["must"].append(
            {"term": {"title.keyword": title}})
    if author:
        query["query"]["bool"]["must"].append({"match": {"author": author}})
    if abstract:
        query["query"]["bool"]["must"].append(
            {"match": {"abstract": abstract}})
    result = ES.search(index=INDEX_NAME, body=query)
    return result.body['hits']


@app.route("/vectorPage")
def vectorPage():
    print("vectorPage")
    size = request.args.get('size')
    keyword = request.args.get('keyword')

    qReq = {"queries": [keyword]}
    res = requests.post(url="http://xx.xx.xx.158:8902/query",
                        data=json.dumps(qReq))
    vector = json.loads(json.loads(res.content)['q_embeddings'])
    vReq = {"name": "title", "k": size, "embedding": vector[0]}
    res = requests.post(
        url="http://xx.xx.xx.3:8862/faiss_vs/search", data=json.dumps(vReq))
    vIds = json.loads(res.content)['indices']

    query = {
        "query": {
            "terms": {
                'title_vector_id': vIds
            }
        }
    }
    result = ES.search(index=INDEX_NAME, body=query)
    return result.body['hits']


@app.route("/getOlPaperById")
def getById():
    pId = request.args.get("id")
    result = ES.get(index=INDEX_NAME, id=pId)
    return result.body


@app.route("/multiSource")
def multiSource():
    keyword = request.args.get('keyword')
    size = request.args.get('size')
    search = arxiv.Search(
        query=keyword,
        max_results=int(size),
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    retResult = []
    for result in search.results():
        paper = {}
        paper['id'] = result.entry_id.replace("http://arxiv.org/abs/","")
        paper['update'] = result.updated
        paper['published'] = result.published
        paper['title'] = result.title
        paper['authors'] = ", ".join(str(author) for author in result.authors)
        paper['abstract'] = result.summary
        paper['comment'] = result.comment
        paper['journal_ref'] = result.journal_ref
        paper['doi'] = result.doi
        paper['primary_category'] = result.primary_category  
        paper['categories'] = result.categories
        paper['links'] = ", ".join(str(link) for link in result.links)
        paper['url'] = result.pdf_url+".pdf"
        retResult.append(paper)
        
    return  {"data":retResult}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
