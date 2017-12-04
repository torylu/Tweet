import boto3
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def analyzeSentiment():
	consumer = KafkaConsumer("Tweets", bootstrap_servers="localhost:9092",
                             consumer_timeout_ms=-1, group_id = None, auto_offset_reset='earliest')
	sns = boto3.client('sns',aws_access_key_id= "AKIAIATAPMMA73TOWOVA",aws_secret_access_key="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", region_name = "us-east-1")
	arn = "arn:aws:sns:us-east-1:663496630551:Tweets"
	

	for message in consumer:
		# print(message)
		try:
			tweetContent = json.loads(json.dumps(message.value))
			if not is_json(tweetContent):
				continue
			tweetContent = json.loads(tweetContent)
			natural_language_understanding = NaturalLanguageUnderstandingV1(username="9946c37a-5efd-4905-8de1-2974a8231f84",password="HiLXF7Vjm5oT",version="2017-02-27")
			response = natural_language_understanding.analyze(
						  text=tweetContent['text'],
						  features=Features(sentiment = SentimentOptions())
						)
			response = json.loads(json.dumps(response))
			score = response['sentiment']['document']['score']
			print(score)
			tweetResponse = {
				'User':tweetContent['user'],
				'Score': score,
				'Longitude': tweetContent['longitude'],
				'Latitude': tweetContent['latitude'],
				'Text': tweetContent['text']
			}
			sns.publish(TopicArn=arn,Subject="Tweet",MessageStructure="json",Message=json.dumps({"default":json.dumps(tweetResponse)}))
		except Exception, e:
			continue
		

def is_json(message):
	try:
		res = json.loads(message)
	except Exception, e:
		return False;
	else:
		return True;
	finally:
		pass

if __name__ == '__main__':
	analyzeSentiment()
	# awsauth = AWS4Auth("AKIAIATAPMMA73TOWOVA", "qCrRf8GKiJBlNuMnzIaAYBZ9aTAy/PsoqqkI9Crk", 'us-east-1', 'es')
	# es = Elasticsearch(hosts = [{'host': "search-twittmap-for-tory-crewiplf7dscv7b6caobny7wui.us-east-1.es.amazonaws.com", 'port': 443}],http_auth = awsauth,use_ssl = True,verify_certs = True,connection_class = RequestsHttpConnection,timeout = 10)

	# res = es.search(index="tweets", body={"query": {"wildcard": {"Text":'*'+ 'technology' +'*'}}}, size=400)
	# tweets = res['hits']['hits']
	# response = []
	# print(tweets)