import re
import spacy
import pickle as pkl
import numpy as np
import tensorflow as tf

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


# load CNN model and preprocessing
with open('static/neural_preprocessing', 'rb') as file_in:
	neural_preprocessing = pkl.load(file_in)
	tokenizer = neural_preprocessing['tokenizer']
	max_sequence_length = neural_preprocessing['max_sequence_length']

cnn = load_model('static/model_cnn')
graph = tf.get_default_graph()
nlp = spacy.load('en')


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