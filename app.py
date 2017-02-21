"""
 A python flask application to scroll through a kanji database
"""

import os

# pylint: disable=import-error
from flask import Flask, request, render_template, make_response
import psycopg2

APP = Flask(__name__)

@APP.route('/')
def index():
    """ Main page, displays all kanji groups. """
    return render_template('main.html')


@APP.route('/<selection>/<level>', methods=['POST', 'GET'])
def db_level(selection=None, level=None):
    """ Category page, displays a particular grade or JLPT level. """

    if request.method == 'POST':
        selection = request.form.split(' ')[0]
        level = request.form.split(' ')[1]

    conn = psycopg2.connect(database='kanji', user=os.environ.get('POSTGRESQL_USER'),\
                            host=os.environ.get('POSTGRESQL_SERVICE_HOST'),\
                            password=os.environ.get('POSTGRESQL_PASSWORD'))
    cur = conn.cursor()
    cur.execute("""SELECT kanj, von, vkun, transl FROM info WHERE %s = %s""" % (selection, level))

    rows = cur.fetchall()
    result_string = ''
    k_list = []
    for row in rows:
        result_string += row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3]
        k_list.append(row[0])

    response = make_response(render_template('flashcard.html', kanji_list=k_list))
    response.headers['u_level'] = level
    response.headers['u_selection'] = selection
    return response


@APP.route('/<selection>/<level>/<kanji>', methods=['POST', 'GET'])
def db_kanji(kanji=None):
    """ Category page, displays a particular grade or JLPT level. """

    if request.method == 'POST':
        kanji = request.form.split(' ')[0]

    conn = psycopg2.connect(database='kanji', user=os.environ.get('POSTGRESQL_USER'),\
                            host=os.environ.get('POSTGRESQL_SERVICE_HOST'),\
                            password=os.environ.get('POSTGRESQL_PASSWORD'))
    cur = conn.cursor()
    cur.execute("""SELECT kanj, von, vkun, transl FROM info WHERE kanj = %s""" % kanji)

    rows = cur.fetchall()

    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3] + "</h3>"

    return  result_string


def split_space(string):
    """ For use with jinja2 filters. """
    return string.strip().split()


if __name__ == '__main__':
    APP.jinja_env.filters['split_space'] = split_space
    APP.run(host='0.0.0.0', port=8080, debug=True)
