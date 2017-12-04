from __future__ import print_function
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

awsauth = AWS4Auth("AKIAIATAPMMA73TOWOVA", "qCrRf8GKiJBlNuMnzIaAYBZ9aTAy/PsoqqkI9Crk", 'us-east-1', 'es')
es = Elasticsearch(hosts = [{'host': "search-twittmap-for-tory-crewiplf7dscv7b6caobny7wui.us-east-1.es.amazonaws.com", 'port': 443}],http_auth = awsauth,use_ssl = True,verify_certs = True,connection_class = RequestsHttpConnection,timeout = 10)

def lambda_handler(event, context):
	data = json.dumps(event, indent = 2)
	data = json.loads(data)
	tweets = res['hits']['hits']

	response = []
	if tweets:
		for tweet in tweets:
			item = {}
			item['latitude'] = hit['_source']['latitude']
			item['longitude'] = hit['_source']['longitude']
			item['sentiment_score'] = hit['_source']['score']
			item['tweet_text'] = hit['_source']['text']

			response.append(item)
	return response
print(json.dumps(es.search(index="twitter", body={"query": {"wildcard": {"text":'*'+'technology'+'*'}}}, size=400)))

    #raise Exception('Something went wrong')
