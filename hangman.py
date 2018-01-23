from flask import Flask,render_template,request,flash,session,redirect, url_for
import sqlalchemy as sql
from passlib.hash import pbkdf2_sha256
import random

# Initiation
db_string = ""
db = sql.create_engine(db_string)
username = ''
app = Flask(__name__)
app.secret_key = 'some_secret'
SESSION_TYPE = 'redis'

# Index Page
@app.route('/')
def index():
	if 'user'in session:
		username = session['user']
		return redirect(url_for('game'))
	return redirect(url_for('auth'))

# Login/Signup Page
@app.route('/auth',methods=['POST','GET'])
def auth():
	if 'user'in session:
		username = session['user']
		return redirect(url_for('game'))
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if request.form['action'] == 'signup':
			result_set = db.execute("SELECT * FROM credentials c WHERE c.username = %s",username)  
			rows = result_set.fetchall()
			if len(rows):
				error = 'Username already exists!!'
			else:
				db.execute("INSERT INTO credentials (username,password) VALUES(%s,%s)",username,pbkdf2_sha256.hash(password))
				session['user'] = username
				return redirect(url_for('game'))
		elif request.form['action'] == 'login':
			result_set = db.execute("SELECT * FROM credentials c WHERE c.username = %s",username)
			rows = result_set.fetchall()
			if not len(rows):
				error = 'Invalid username or password!!'
			else:
				hash_pass = rows[0][1]
				if not pbkdf2_sha256.verify(password, hash_pass):
					error = 'Invalid username or password!!'
				else:
					session['user'] = username
					return redirect(url_for('game'))

	return render_template("login.html",error=error)

# Get a new word for a new round
@app.route('/new_word', methods = ['GET'])
def get_post_javascript_data():
    new_word = gen_word()
    return new_word

# Check the score, update DB if necessary
@app.route('/score', methods = ['POST'])
def score():
	username = session['user']
	score = request.form['score']
	result_set = db.execute("SELECT s.score FROM scores s WHERE s.username = %s",username)
	rows = result_set.fetchall()
	if not len(rows):
		db.execute("INSERT INTO scores (username,score) VALUES(%s,%s)",username,score)
	else:
		if rows[0][0] > int(score):
			return 'Success'
		else:
			db.execute("UPDATE scores SET score=%s WHERE username = %s",score,username)
	return 'Success'

# Logout
@app.route('/logout', methods = ['POST'])
def logout():
	session.pop('user', None)
	return redirect(url_for('auth'))

# Game Page
@app.route('/game',methods=['POST','GET'])
def game():
	if 'user'in session:
		username = session['user']
	else:
		return redirect(url_for('auth'))
	best = 0
	word = gen_word()
	result_set = db.execute("SELECT s.score FROM scores s WHERE s.username = %s",username)
	rows = result_set.fetchall()
	if len(rows):
		best = rows[0][0]
	print best
	return render_template("game.html",word = word,best=best)

# Get a random word from the file
def gen_word():
	c = 0
	f = open("english_words.txt","r")
	ran = random.randint(0,416289)
	for line in f:
		if c == ran:
			new = line.strip()
			break
		c += 1
	return new

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80)









