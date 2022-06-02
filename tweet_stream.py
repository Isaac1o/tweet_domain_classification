import pandas as pd
import tweepy
import boto3
import os
import time
from utility.tweepy_helper import *


class Streamer(tweepy.StreamingClient):
    def __init__(self, bearer_token, **kwargs):
        super().__init__(bearer_token, **kwargs)
        self.tweet_fields = ['lang', 'context_annotations']

    def on_response(self, response):
        # Check to see if tweet is in english and has domain labels
        if response.data.data['lang'] == 'en' and response.data.data.get('context_annotations'):
            text = response.data.data['text']
            # If tweet is a retweet then look at the referenced tweet because RTs are truncated
            if text.startswith('RT'):
                try:
                    text = response.includes['tweets'][0]['text']
                except:
                    pass

            # There may be multiple domains for each tweet. Iterate through all domains and concat into string.
            domains = set()
            for domain_data in response.data.data['context_annotations']:
                domains.add(domain_data['domain']['name'])

            domains = '<COMMA>'.join(domains)

            data = f'{bytes(text, "utf-8")}<COMMA>{domains}\n'
            print(data)

            # Send data to AWS
            try:
                client.put_record(
                    DeliveryStreamName=DELIVERY_STREAM,
                    Record={'Data': data}
                )
            except Exception as e:
                print(e)
                print('Failed to stream data')

    def on_errors(self, errors):
        pass


if __name__ == '__main__':
    # AWS client for kinesis firehose
    client = boto3.client(
        'firehose',
        region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_NLP'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY_NLP']
    )
    DELIVERY_STREAM = 'DeepLearningTweetStream'

    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAJI7ZAEAAAAAfn%2Br3vNXQFCIH6tdU7j%2BwkbA9yA%3Dtzlg2QSiF7WLF876wpskwukQzXBxNK7BmNKTqjkMOs3Lw6qsOE'
    stream = Streamer(BEARER_TOKEN)
    while True:
        try:
            print('Streaming...')
            stream.sample(tweet_fields=['lang', 'context_annotations'], expansions='referenced_tweets.id')
        except Exception as e:
            print(e)
            print('Disconnected...')
            time.sleep(3)
            print('Reconnecting...')
