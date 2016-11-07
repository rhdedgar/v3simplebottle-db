import os

from flask import Flask, request
import psycopg2


app = Flask(__name__)



@app.route('/')
def index():
    all_buttons = (
        '<button type=\"submit\" name="submit" value="school 1">Grade 1</button>\n'
        '<button type=\"submit\" name="submit" value="school 2">Grade 2</button>\n'
        '<button type=\"submit\" name="submit" value="school 3">Grade 3</button>\n'
        '<button type=\"submit\" name="submit" value="school 4">Grade 4</button>\n'
        '<button type=\"submit\" name="submit" value="school 5">Grade 5</button>\n'
        '<button type=\"submit\" name="submit" value="school 6">Grade 6</button>\n'
    )
    
    #submitted = request.form['submit']
    #selection = submitted.split((' ')[0])
    #level = submitted.split((' ')[1])
    
    return all_buttons


@app.route('/<selection>/<level>')
def db_query(selection, level):

    conn = psycopg2.connect(database='kanji', user=os.environ.get('POSTGRESQL_USER'), host=os.environ.get('POSTGRESQL_SERVICE_HOST'), password=os.environ.get('POSTGRESQL_PASSWORD'))
    cur = conn.cursor()
    cur.execute("""SELECT kanj, von, vkun, transl from info WHERE %s = %s""" % (selection, level))

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3] + "</h3>"

    return  result_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

