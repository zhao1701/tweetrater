from flask import Flask, redirect, url_for, request, render_template
from helpers import tweet_rater

app = Flask('__main__')

@app.route('/')
def index():
	return render_template('test_index.html')

@app.route('/predict/', methods = ['POST'])
def predict():
	tweet = request.form['tweet']
	return tweet + '<br/>' + tweet_rater(tweet)

if __name__ == '__main__':
	app.run(debug=True)