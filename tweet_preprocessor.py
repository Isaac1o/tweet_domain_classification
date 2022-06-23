import pandas as pd
import numpy as np
import sys
import os
import ast  # Used to read byte literals
import boto3


def get_files(client, bucket_name, prefix):
    # Returns all files with data
    paginator = client.get_paginator('list_objects_v2')
    response = paginator.paginate(Bucket=bucket_name, Prefix=prefix, PaginationConfig={"PageSize": 1000})
    all_files = []
    for page in response:
        files = page.get('Contents')
        for file in files:
            all_files.append(file['Key'])

    return all_files


def parse_data(filepath):
    rows = []
    with open(filepath, 'r') as f:
        for s in f.readlines():
            row = s.split('<COMMA>')
            row = process_row(row)
            rows.append(row)

    return rows


def process_row(row):
    # The first element of the row is a byte string
    row[0] = ast.literal_eval(row[0]).decode('utf-8')
    return [elem.strip('\n') for elem in row]


def join_rows(main_rows, additional_rows):
    return np.concatenate([main_rows, additional_rows])


if __name__ == '__main__':
    # file = sys.argv[1]
    s3_client = boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_NLP'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY_NLP']
    )
    BUCKET = 'deeplearningtweetdata'
    PREFIX = 'data/multi_label/'
    files = get_files(s3_client, BUCKET, PREFIX)
    print(files)
