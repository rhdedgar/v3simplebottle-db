__author__ = 'spousty'

import psycopg2
from bottle import route, run
import os

@route('/')
def index():
	return "<h1> hello OpenShift Ninja with DB</h1>"

@route('/db')
def dbexample():
	try:
		#TODO change the connection info to env variables
		conn = psycopg2.connect(dbname='db', user=os.environ.get('POSTGRESQL_USER'), host=os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST'), password=os.environ.get('POSTGRESQL_PASSWORD'))
	except:
		return os.environ.get('POSTGRESQL_USER') + "  " + os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST')
	
	cur = conn.cursor()
	cur.execute("""SELECT * from users""")
	
	rows = cur.fetchall()
	result_string = "Here are your results: \n"
	for row in rows:
		result_string += row[0] + "\n"

	return "<h2> " + result_string + "</h2>"

if __name__ == '__main__':
	run(host='0.0.0.0', port=8080)
