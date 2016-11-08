import os

from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/<selection>/<level>', methods=['POST', 'GET'])
def db_query(selection=None, level=None):

    if request.method == 'POST':
        selection = request.form.split(' ')[0]
        level = request.form.split(' ')[1]
    conn = psycopg2.connect(database='kanji', user=os.environ.get('POSTGRESQL_USER'), host=os.environ.get('POSTGRESQL_SERVICE_HOST'), password=os.environ.get('POSTGRESQL_PASSWORD'))
    cur = conn.cursor()
    cur.execute("""SELECT kanj, von, vkun, transl FROM info WHERE %s = %s""" % (selection, level))

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3] + "</h3>"

    return  result_string


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

