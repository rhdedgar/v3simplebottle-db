__author__ = 'spousty'

import psycopg2
from bottle import route, run

@route('/')
def index():
    return "<h1> hello OpenShift Ninja</h1>"
    
@route('/db')
def dbexample():
	try:
	#TODO change the connection info to env variables
		conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
	except:
		print "I am unable to connect to the database"	
	
	cur = conn.cursor()
	cur.execute("""SELECT * from users""")
	
	rows = cur.fetchall()
	result_string = "Here are your results: \n"
	for row in rows:
    	result_string += row[2] + "\n"
    	
	return "<h2> " + result_string + "</h2>"

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
