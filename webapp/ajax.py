from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/home/', methods=['GET', 'POST'])
def home():
	return render_template('ajax_index.html')

@app.route('/upper/', methods=['GET', 'POST'])
def upper():
	text = request.args.get('text')
	text = text.upper()
	print(text)
	return json.dumps(dict(uppertext=text))

if __name__ == '__main__':
	app.run(debug=True)