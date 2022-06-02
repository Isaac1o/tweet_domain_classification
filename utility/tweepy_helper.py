import tweepy


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with format
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        keys = f.readlines()[1].strip().split(',')

    return keys


def authenticate_research(research_auth_filename, wait_on_rate_limit=False):
    """
    Return twitter Client object for research license
    """
    consumer_key, consumer_secret, access_token, access_token_secret, bearer = loadkeys(research_auth_filename)
    client = tweepy.Client(bearer_token=bearer,
                           consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret,
                           return_type='response',  # Returns python dictionary instead of response object
                           wait_on_rate_limit=wait_on_rate_limit)  # Whether to wait when rate limit is reached
    return client




