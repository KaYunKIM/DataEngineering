
from google.oauth2 import service_account
from google.cloud import pubsub_v1

from concurrent import futures
from decouple import config
import tweepy
import json


key_path = "twitter-pubsub-ec2db1065872.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


# TODO(developer)
project_id = "twitter-pubsub"
topic_id = "tweets"

twitter_api_key = config('api_key')
twitter_api_secret_key = config('api_secret_key')
twitter_access_token = config('access_token')
twitter_access_token_secret = config('access_token_secret')


# Configure the batch to publish as soon as there are 10 messages
# or 1 KiB of data, or 1 second has passed.
batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=100,  # default 100
    # max_bytes=1024,  # default 1 MiB
    max_latency=30,  # default 10 ms
)
publisher = pubsub_v1.PublisherClient(batch_settings, credentials=credentials)
topic_path = publisher.topic_path('twitter-pubsub', 'tweets')  # pjt, topic
publish_futures = []


# Resolve the publish future in a separate thread.
def callback(future: pubsub_v1.publisher.futures.Future) -> None:
    message_id = future.result()
    # timestamp = future.result()
    print('message_id', message_id)

class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print('messae: ', status)
        # num of threads
        for i in range(10):
            tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
            # Data must be a bytestring
            data = tweet.encode("utf-8")
            print('data: ', data)
            publish_future = publisher.publish(topic_path, data)
            # Non-blocking. Allow the publisher client to batch multiple messages.
            publish_future.add_done_callback(callback)
            publish_futures.append(publish_future)
            print()
        
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        print(f"Published messages with batch settings to {topic_path}.")

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