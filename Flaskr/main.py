from flask import Flask, render_template, flash, redirect, url_for, g, request, session
import sqlite3, time, smtplib
from contextlib import closing
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#configuration

SECRET_KEY = 'cake-is-a-lie'
DEBUG = True
DATABASE = 'C:\\Python27\\Stuff\\flaskr\\tmp\\flaskr.db'
USERNAME = 'admin'
PASSWORD = 'foobar'

#initialization 

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def create_table():
	with closing(connect_db()) as conn:
		with app.open_resource('schema.sql', mode = 'r') as file:
			conn.cursor().executescript(file.read())
		conn.commit()

	print('Tables created.')

def fetch_user(uname):
	conn = connect_db()
	conn.row_factory = sqlite3.Row
	curs = conn.cursor()
	curs.execute('select * from users where username = (?)', [str(uname)])
	return curs.fetchall()

def send_mail(toAddr, uname, pword):
	fromAddr = 'noreply.server442@gmail.com'
	data = MIMEMultipart()
	data['From'] = fromAddr
	data['To'] = toAddr
	data['Subject'] = 'You have successfully registered.'
	data.attach(MIMEText('Thank you for registering. Your username and password are %s and %s.' % (uname, pword))) 

	server = smtplib.SMTP('smtp.gmail.com:587') 
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('noreply.server442', 'testaccount42')
	server.sendmail(fromAddr, toAddr, str(data))
	server.quit()

create_table()

#views 

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(error):
	if hasattr(g, 'db'):
		g.db.close()

@app.route('/')
def show_posts():
	g.db.row_factory = sqlite3.Row  #Query performed on g.db instead of making a separate connection. 
	curs = g.db.cursor()
	curs.execute('select title, content, date from posts order by pid desc')
	posts = []
	for thing in curs.fetchall():
		posts.append(dict(title = thing[0], content = thing[1], date = thing[2]))

	return render_template('main.html', posts = posts)

@app.route('/add', methods = ['POST'])
def add_post():
	if not session['logged_in']:
		abort(401)
	dbase = g.db	
	dbase.cursor().execute('insert into posts(title, content, date) values (?, ?, ?)', [request.form['title'], request.form['content'], str(time.strftime('%c'))]) 
	dbase.commit()
	flash('New post successfully added.')
	return redirect(url_for('show_posts'))

#error = None
#@app.route('/login', methods = ['GET', 'POST']) #Where is GET used? 
#def login():
#	if request.method == 'POST':
#		global error
#		error = None
#		if request.form['username'] != app.config['USERNAME']:
#			error = 'Invalid Username'
#		elif request.form['password'] != app.config['PASSWORD']:
#			error = 'Invalid Password'
#		else:
#			session['logged_in'] = True
#			flash('Login successful.')
#			return redirect(url_for('show_posts'))
#
#	return render_template('login.html', error = error)  

errorRegister = None
errorLogin = None 

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		global errorRegister
		if len(fetch_user(request.form['username'].lower())) != 0: 
			errorRegister = 'Username already exists. Please enter another.'
		elif request.form['password'] != request.form['confirm']:
			errorRegister = 'Your passwords do not match.'
		else:
			dbase = g.db
			dbase.cursor().execute('insert into users(username, password, email) values (?, ?, ?)', [request.form['username'], request.form['password'], request.form['email']])
			dbase.commit()
			send_mail(request.form['email'], request.form['username'], request.form['password'])
			flash('Registration successful. You may login now. An email has been sent to your email address.')   
			return redirect(url_for('login'))

	return render_template('register.html', error = errorRegister)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		global errorLogin
		if len(fetch_user(request.form['username'].lower())) == 0:
			errorLogin = 'Invalid Username'
		elif fetch_user(request.form['username'].lower())[0][2] != request.form['password']:
			errorLogin = 'Invalid Password'
		else:
			session['logged_in'] = True
			flash('Login successful.')
			return redirect(url_for('show_posts'))
	return render_template('login.html', error = errorLogin)








@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Logout successful.')
	return redirect(url_for('show_posts'))




#running 

if __name__ == '__main__':
	app.run()




