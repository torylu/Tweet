from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from kafka import SimpleProducer, KafkaClient
import sys, json, requests
import tweepy, json
import random


consumer_key = "wcY8KyVWGb4GcpFqs4t40RYwI"
consumer_secret = "G7x2WmbOZkyxd7gwB2gOgKy4ofRKlIq1H1txpTmMayYOnhQZjj"
access_token = "934147509223673857-VpbBYn28QuUlkGOX55XNtGvI8bbkUoi"
access_token_secret = "NK1svKINtJFiKUwfuxq7aQ5Tsa2pXqbSbwtGvIDb0k1J2"

class StreamListener(tweepy.StreamListener):
	
	def __init__(self, api):
		self.api = api
		client = KafkaClient("localhost:9092")
		self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = 1000,
                          batch_send_every_t = 10)

	def on_status(self, status):

		if status.coordinates == None:
			lat = random.uniform(-90, 90)
			lon = random.uniform(-180, 180)
		else:
			print(status.coordinates)
			lat = status.coordinates['coordinates'][1]
			lon = status.coordinates['coordinates'][0]
			print(lat)
		tweet = {
			"user": status.user.id,
			"text": status.text,
			"latitude": lat,
			"longitude": lon
		}
		# print(json.dumps(tweet))
		# print(es.index(index="twitter", doc_type='tweet', id=2, body=json.dumps(tweet)))
		self.producer.send_messages(b'Tweets', json.dumps(tweet))
		return True;


	def on_error(self, status_code):
		if status_code == 420:
		    return False


def streamingFromTweet():
	auth = tweepy.OAuthHandler("wcY8KyVWGb4GcpFqs4t40RYwI", "G7x2WmbOZkyxd7gwB2gOgKy4ofRKlIq1H1txpTmMayYOnhQZjj")
	auth.set_access_token(access_token, access_token_secret);
	API = tweepy.API(auth)
	stream_listener = StreamListener(API)
	stream = tweepy.Stream(auth=auth, listener=stream_listener)
	stream.filter(track=["technology", "index Fund", "financial"])
   	return res

if __name__ == '__main__':
	streamingFromTweet()

