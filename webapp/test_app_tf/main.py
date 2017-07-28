from flask import Flask, redirect, url_for, request, render_template, jsonify, Markup
from helpers import *
from sklearn.metrics import accuracy_score

app = Flask(__name__)

test_tweets = pd.Series()

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/predict/', methods=['GET','POST'])
def predict():
	tweet = request.args.get('tweet')
	rating, prediction = tweet_rater(tweet)
	return jsonify(prediction=prediction, rating=int(rating))

@app.route('/challenge/')
def challenge():
	global test_tweets
	test_tweets = pd.Series()
	return render_template('challenge.html')

@app.route('/challenge/get_training/')
def get_training():
	rating = int(request.args.get('rating'))
	n_samples = int(request.args.get('n_samples'))
	return jsonify(training_samples=get_training_samples(rating=rating, n_samples=n_samples))

@app.route('/challenge/get_test/')
def get_test():
	n_tweets = int(request.args.get('n_tweets'))
	global test_tweets
	test_tweets = get_test_samples(n_tweets)
	return jsonify(test_tweets=test_tweets.values.tolist())

@app.route('/results/', methods = ['POST'])
def results():
	y_cnn_sample = y_pred.reindex(test_tweets.index).astype(str)
	y_test_sample = y_test.reindex(test_tweets.index).astype(str)
	cnn_accuracy = accuracy_score(y_cnn_sample, y_test_sample) * 100

	n_answers = len(request.form)
	y_user_sample = [request.form['user-label-{}'.format(i)] for i in range(n_answers)]
	y_user_sample = pd.Series(y_user_sample, index = test_tweets.index)
	user_accuracy = accuracy_score(y_user_sample, y_test_sample) * 100

	zipped_list = zip(test_tweets, y_user_sample, y_cnn_sample, y_test_sample)
	answer_map = {\
		'0': Markup("<span class='glyphicon glyphicon-ok-sign'></span>"), 
		'1': Markup("<span class='glyphicon glyphicon-exclamation-sign'></span>"),
		'2': Markup("<span class='glyphicon glyphicon-remove-sign'></span>")}

	return render_template('results.html', zipped_list=zipped_list,
		model_accuracy=cnn_accuracy, user_accuracy=user_accuracy, legend=answer_map)

@app.route('/about/')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True, port=5000)