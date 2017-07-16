from flask import Flask, redirect, url_for, request, render_template, jsonify
from helpers import tweet_rater

app = Flask('__main__')

@app.route('/home/', methods=['GET','POST'])
def index():
	return render_template('test_index.html')

@app.route('/predict/', methods = ['GET','POST'])
def predict():
	tweet = request.args.get('tweet')
	return jsonify(prediction=tweet_rater(tweet))

if __name__ == '__main__':
	app.run(debug=True)