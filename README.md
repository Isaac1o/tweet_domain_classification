# Deep Learning NLP Project

## Goal
Tweets contain a lot of information regarding different topics. We can agree that you can use multiple key
words to explain a tweet. Twitter's api has an option to return the domain/entity of a tweet.
For example, if we have a tweet: "I took my dog on a walk outside today. We also stopped by the 
store to get groceries", we could label this tweet with different key words like "Pet", "Shopping",
"Outdoors", etc.

We will use this feature the Twitter API provides to collect our training data: tweet and label(s).
We'll then build and train a neural network to classify the tweets. This is a multi label classification problem.

## Data Acquisition
Collect a balanced and unbiased dataset we need to collect tweets randomly. Unfortunately,
Twitter's API does not allow the random collection of historic tweet (there must be some sort
of keyword). However, Twitter allows you to stream random tweets.

We've build a simple script to stream random english tweets to an AWS S3 bucket to build a corpus
of tweets for training. Currently, the stream is collecting about 1,500 tweets every 5 minutes.
After a couple of days we should have a sizable collection of tweets to work with.

Lastly, the tweet stream will be deployed to an AWS EC2 instance for continuous streaming.

### Labels
![Labels](static/domain_labels.png)

## Data
The data is streamed to an AWS S3 bucket and stored in a text file. The data format is as follows for each tweet:
`text_in_bytes<COMMA>label_1<COMMA>label_2<COMMA>label_n`

For this project we used 1M tweets and performed a 80-20 train test split.

## Modeling
The goal for this project is to train a deep learning text classification model. The two architectures used are RNN and LSTM.

### RNN
Recurrent Neural Network is the most basic neural network architecture that handles sequential data for text classification tasks. It maintains a hidden state which is used to make predictions and is updated after every token in a sequence. A common disadvantage of RNN's are that they can't handle long term memory very well. 

Our fixed hyper-parameters:
- Number pochof epochs  = 5
- ReLU layer
- Number of linear layers = 2

Our adjusted hyper-parameters:
- Learning Rate
- Word embedding size
- Hidden layer size

Below are the results for the different RNN models. 


### LSTM
Long short-term memory models work excellent for a sequence based text classification task like this one. Due to the LSTM's "cell", this neural network is able to remember values over arbitrary time intervals unlike a RNN.

To make the various LSTM models we trained comparable, we kept some hyper-parameters fixes:
- Dropout = 0.3
- Learning rate = 0.01
- Epoches = 5
- Batch size = 10,000
- Relu activation function

These are the hyper-parameters that we adjusted:
- Word embedding size
- LSTM hidden size
- Number of LSTM layers
- Number of linear layers

Here are the results of the different models trained.

![LSTM Results](https://github.com/Isaac1o/tweet_domain_classification/blob/main/static/Screen%20Shot%202022-06-29%20at%2011.17.47%20PM.png)

[LSTM Notebook](https://github.com/Isaac1o/tweet_domain_classification/blob/main/notebooks/04_Isaac_Lo_LSTM.ipynb)


