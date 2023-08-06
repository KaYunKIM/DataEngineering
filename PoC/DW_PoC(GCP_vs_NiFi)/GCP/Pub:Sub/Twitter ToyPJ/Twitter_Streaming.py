from decouple import config
import tweepy
import json

from google.cloud import pubsub_v1
from google.oauth2 import service_account

key_path = "twitter-pubsub-ec2db1065872.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Connection to Pub/Sub topic
client = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = client.topic_path('twitter-pubsub', 'tweets')  # pjt, topic

twitter_api_key = config('api_key')
twitter_api_secret_key = config('api_secret_key')
twitter_access_token = config('access_token')
twitter_access_token_secret = config('access_token_secret')


class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)
        tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
        client.publish(topic_path, data=tweet.encode('utf-8'))

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

stream_listener = SimpleStreamListener()

# Connection to Twitter
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['data'])




# BUCKET_NAME=dataflow_streaming_pipeline
# PROJECT_ID=$(gcloud config get-value project)
# TOPIC_ID=tweets
# REGION=us