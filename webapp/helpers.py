import re
import en_core_web_sm
import pickle as pkl
import numpy as np
import pandas as pd

# using theano backend
from keras.models import load_model, model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


# load preprocessing objects
with open('static/neural_preprocessing', 'rb') as file_in:
	neural_preprocessing = pkl.load(file_in)

    # a pre-fit tokenizer takes an input string and returns a list of indexes
	tokenizer = neural_preprocessing['tokenizer']

    # used to specify how to pad a tweet's token vector
	max_sequence_length = neural_preprocessing['max_sequence_length']

# load CNN model and NLP language models
with open('static/cnn_model_architecture.json', 'rt') as file_in:
    architecture = file_in.read()
    cnn = model_from_json(architecture)
    cnn.load_weights('static/cnn_model_weights.h5')
    nlp = en_core_web_sm.load()

### TWEETRATER ###

# tweet-cleaning functions
replace_user = lambda tweet: re.sub(r'(@\w+\s*)', r'TWITTER_HANDLE ', tweet)
clean_tweet = lambda tweet: re.sub(r'#|&|\(|\)|\"|(https?://\S*)|(�\S*\d*)|(128\d{3})|(_*UNDEF)', ' ', tweet)

# predict offensiveness of tweet
def tweet_rater(tweet):
    '''
    This function uses the string of an unprocessed tweet to return a tuple consisting of:
        1) a rating from [0,2] corresponding to whether the tweet is normal, offensive, or hate speech
        2) a statement about the model's classification prediction and confidence
    '''

    # clean and lemmatize tweet
    tweet = clean_tweet(tweet)
    tweet_tokens = [token.lemma_ for token in nlp(tweet)]
    tweet = ' '.join(tweet_tokens)

    # convert tweet to vector of indexes and provide right-side padding
    x_vect = tokenizer.texts_to_sequences([tweet])
    x_vect = pad_sequences(x_vect, maxlen = max_sequence_length, padding = 'post', truncating = 'post')

    # get from model a vector of classification probabilities and use probas to determine rating
    probas = cnn.predict(x_vect)[0]
    rating = np.argmax(probas)
    if rating == 0:
        return rating, 'I\'m {:2.4}% sure that\'s not offensive.'.format(probas[0]*100)
    elif rating == 1:
        return rating, 'I\'m {:2.4}% sure that\'s offensive.'.format(probas[1]*100)
    else:
        return rating, 'I\'m {:2.4}% sure that\'s hate speech.'.format(probas[2]*100)

### CHALLENGE ###

# load training and test data
with open('static/data_all', 'rb') as file_in:
    data_all = pkl.load(file_in)
    df_orig = data_all['df_orig']
    X_train = data_all['X_train']
    y_test = data_all['y_test']

    df_orig_train = df_orig.reindex(X_train.index)
    df_orig_test = df_orig.reindex(y_test.index)

with open('static/cnn_predictions', 'rb') as file_in:
    y_pred = pkl.load(file_in)

def get_training_samples(n_samples=10, rating=0, data=df_orig_train):
    return data[data.rating == rating].text.sample(n_samples).values.tolist()

def get_test_samples(n_samples=10, data=df_orig_test):
    return data.text.sample(n_samples)