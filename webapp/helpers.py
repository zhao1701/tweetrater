import re
import spacy
import pickle as pkl
import numpy as np
import pandas as pd

from tensorflow import get_default_graph
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


# load CNN model and preprocessing
with open('static/neural_preprocessing', 'rb') as file_in:
	neural_preprocessing = pkl.load(file_in)
	tokenizer = neural_preprocessing['tokenizer']
	max_sequence_length = neural_preprocessing['max_sequence_length']

cnn = load_model('static/model_cnn')
graph = get_default_graph()
nlp = spacy.load('en')

### TWEET RATER ###

# tweet-cleaning functions
replace_user = lambda tweet: re.sub(r'(@\w+\s*)', r'TWITTER_HANDLE ', tweet)
clean_tweet = lambda tweet: re.sub(r'#|&|\(|\)|\"|(https?://\S*)|(�\S*\d*)|(128\d{3})|(_*UNDEF)', ' ', tweet)


# predict offensiveness of tweet
def tweet_rater(tweet):
    tweet = clean_tweet(tweet)
    tweet_tokens = [token.lemma_ for token in nlp(tweet)]
    tweet = ' '.join(tweet_tokens)
    #print(tweet)
    x_vect = tokenizer.texts_to_sequences([tweet])
    x_vect = pad_sequences(x_vect, maxlen = max_sequence_length, padding = 'post', truncating = 'post')
    with graph.as_default():
    	probas = cnn.predict(x_vect)[0]
    #print(probas)
    rating = np.argmax(probas)
    if rating == 0:
        return 'I\'m {:2.4}% sure that\'s not offensive.'.format(probas[0]*100)
    elif rating == 1:
        return 'I\'m {:2.4}% sure that\'s offensive.'.format(probas[1]*100)
    else:
        return 'I\'m {:2.4}% sure that\'s hate speech.'.format(probas[2]*100)

### BEAT THE MODEL ###

# load training and test data
with open('static/data_all', 'rb') as file_in:
    data_all = pkl.load(file_in)
    df_orig = data_all['df_orig']
    X_train = data_all['X_train']
    y_test = data_all['y_test']

    df_orig_train = df_orig.reindex(X_train.index)
    df_orig_test = df_orig.reindex(y_test.index)

def get_training_samples(n_samples=10, rating=0, data=df_orig_train):
    return data[data.rating == rating].text.sample(n_samples).values

def get_test_samples(n_samples=10, data=df_orig_train):
    return data.text.sample(n_samples).values

print(get_test_samples(5))