from flask import Flask, redirect, url_for, request, render_template, jsonify
from helpers import *

app = Flask('__main__')

test_tweets = pd.Series()

@app.route('/home/', methods=['GET','POST'])
def index():
	return render_template('test_index.html')

@app.route('/predict/', methods = ['GET','POST'])
def predict():
	tweet = request.args.get('tweet')
	return jsonify(prediction=tweet_rater(tweet))

@app.route('/challenge/')
def challenge():
	global test_tweets
	test_tweets = pd.Series()
	return render_template('test_challenge.html')

@app.route('/challenge/get_training/')
def get_training():
	rating = int(request.args.get('rating'))
	n_samples = int(request.args.get('n_samples'))
	return jsonify(training_samples=get_training_samples(rating=rating, n_samples=n_samples))

@app.route('/challenge/get_test/')
def get_test():
	n_tweets = int(request.args.get('n_tweets'))
	new_test_tweets = get_test_samples(n_tweets)
	global test_tweets
	test_tweets = pd.concat([test_tweets, new_test_tweets], axis = 0)
	return jsonify(test_tweets=new_test_tweets.values.tolist())

if __name__ == '__main__':
	app.run(debug=True)