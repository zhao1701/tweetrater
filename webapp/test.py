from flask import Flask, redirect, url_for, request, render_template

app = Flask('__main__')

@app.route('/')
def index():
	return render_template('test_index.html')

@app.route('/display_name/', methods = ['POST'])
def display_name():
	first = request.form['first_name']
	last = request.form['last_name']
	return 'Hello {} {}'.format(first, last)

if __name__ == '__main__':
	app.run(debug=True)