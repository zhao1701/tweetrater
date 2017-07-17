from flask import Flask, redirect, url_for, request, render_template, jsonify
from helpers import *

app = Flask('__main__')

@app.route('/home/', methods=['GET','POST'])
def index():
	return render_template('test_index.html')

@app.route('/predict/', methods = ['GET','POST'])
def predict():
	tweet = request.args.get('tweet')
	return jsonify(prediction=tweet_rater(tweet))

@app.route('/challenge/')
def challenge():
	return render_template('test_challenge.html')

@app.route('/challenge/get_training/')
def get_training():
	rating = int(request.args.get('rating'))
	n_samples = int(request.args.get('n_samples'))
	return jsonify(training_samples=get_training_samples(rating=rating, n_samples=n_samples))

if __name__ == '__main__':
	app.run(debug=True)