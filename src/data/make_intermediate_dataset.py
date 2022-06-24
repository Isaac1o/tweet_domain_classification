import pandas as pd
import numpy as np
import sys
import os
import ast  # Used to read byte literals
import boto3
import tqdm

def get_files(client, bucket_name, prefix):
    # Returns all filenames within bucket
    paginator = client.get_paginator('list_objects_v2')
    response = paginator.paginate(Bucket=bucket_name, Prefix=prefix, PaginationConfig={"PageSize": 1000})
    all_files = []
    for page in response:
        files = page.get('Contents')
        for file in files:
            all_files.append(file['Key'])

    return all_files[1:]


def parse_data(s3_client, bucket, prefix):
    # Loads text file from bucket and parses the file and decodes the tweet
    data = s3_client.get_object(Bucket=bucket, Key=prefix)  # Read data from s3
    contents = data['Body'].read().decode('utf-8')  # Get the data from the data object
    rows = contents.split('\n')

    processed_rows = []
    for row in rows:
        if row.strip() == '':
            continue
        row = row.split('<COMMA>')
        row = process_row(row)
        processed_rows.append(row)

    return processed_rows  # List of tweets and their categories


def process_row(row):
    # The first element of the row is a byte string. This
    row[0] = ast.literal_eval(row[0]).decode('utf-8')
    return [elem.strip('\n') for elem in row]


def join_rows(main_rows, additional_rows):
    return np.concatenate([main_rows, additional_rows])


def make_interm_dataset(save_path):
    # Get all tweets from all text files, parse and decode them, and aggregate them all in one list.
    # Using the list of tweets, create a dataframe and save it
    s3_client = boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_NLP'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY_NLP']
    )
    BUCKET = 'deeplearningtweetdata'
    PREFIX = 'data/multi_label/'

    all_files = get_files(s3_client, BUCKET, PREFIX)  # Get all file paths
    all_data = []
    for file in tqdm.tqdm(all_files[:10]):
        data = parse_data(s3_client, BUCKET, file)
        all_data = all_data + data

    # Put data into a dataframe
    df = pd.DataFrame(all_data)

    df.to_csv(save_path, index=None)
    print(f'Saved to {save_path}')


if __name__ == '__main__':
    path = '../../data/intermediate/interm_tweets.csv'
    make_interm_dataset(path)
