from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# create app
app  = Flask(__name__)
# Add config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:thiraphat2545@localhost:5432/quotes'
# Add config postgreql for HEROKU
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://whiseviaupxhjv:6af0b606541098c0f998e6aeec9c7c9a7e78e5542ce3f9b7357b543253103909@ec2-54-159-22-90.compute-1.amazonaws.com:5432/daq7l5gtegfto5'
# remove notification after add data to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create database from class and add to postgresql quotes database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MyQuote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(30))
	quote = db.Column(db.String(2000))
#use root route decorator
if __name__ == '__main__':
	app.run(debug=True, port=5000)

# create route
@app.route('/')
def index():
	# query with get Alldata to homepage
	result = MyQuote.query.all()
	return render_template('index.html', result=result)

@app.route('/quote')
def quote():
	return render_template('quote.html')

# add redirect to homepage after send data success
# add http method
@app.route('/process', methods =  ['POST'])
def process():
# request from user 
	author = request.form['author']
	quote = request.form['quote']
	# add data to database with class
	quote_data = MyQuote(author=author, quote=quote)
	# add new data
	db.session.add(quote_data)
	# save to database
	db.session.commit()
	return redirect(url_for('index.html'))
    