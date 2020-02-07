from flask import Flask , render_template , redirect , request

from flask_mysqldb import MySQL
from math import floor
import yaml
import string
from random import choice

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

host = "http://localhost:5000/"

def operation(long_url):
	temp = long_url.split('://' , 1)[0]
	if temp == long_url:
		return 'http://' + long_url
	else :
		return long_url

def base10(str):
	bs = 62
	str = str.split('-' , 1)[0]
	base = string.digits + string.ascii_lowercase + string.ascii_uppercase
	length = len(str)
	res = 0 
	for i in range(length):
		res = res * bs + base.find(str[i])
	return res

def base62(num):
	base = string.digits + string.ascii_lowercase + string.ascii_uppercase
	q = num
	bs = 62
	r = q % bs 
	res = base[r]
	q = floor(q / bs)
	while q:
		r = q % bs
		res = base[r] + res
		q = floor(q / bs)
	return res


def make_of_length8(short_url):
	temp_url = short_url
	str = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(7))
	length = len(temp_url)
	if length < 7:
		temp_url += '-'
		++length
	temp_url = temp_url + str[:7 - length - 1]
	return temp_url

def view(long_url):
	long_url = operation(long_url)
	cur = mysql.connection.cursor()
	cnt = 0 
	cur.execute("INSERT INTO users VALUES (%s, %s)" , (0 , long_url))
	mysql.connection.commit()
	cur.execute("select LAST_INSERT_ID()")
	cnt = cur.fetchone()[0]
	cur.close()
	short_url = base62(cnt)
	short_url = make_of_length8(short_url)
	return short_url

@app.route('/' , methods=['GET' , 'POST'])

def index():
	if request.method == 'POST':
		user_details = request.form
		long_url = user_details['longurl']
		short_url = view(long_url)
		return render_template('users.html' , short_url = host + short_url)
	return render_template('index.html')

@app.route('/<short_url>')

def redirect_short_url(short_url):
	ID1 = base10(short_url)
	cur = mysql.connection.cursor()
	cur.execute("SELECT users.longurl FROM users WHERE users.id = '%s'" , (ID1 , ))
	try:
		redirect_url = cur.fetchone()[0]
	except Exception as e:
		return "<h1> wrong url enterered </h1>" + '<a href = "http://localhost:5000"> back </a>'
	return redirect(redirect_url)


if __name__ == '__main__':
	app.run(debug = True)





