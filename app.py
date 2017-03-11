"""
 A python flask application to scroll through a kanji database
"""

import os

# pylint: disable=import-error
from flask import Flask, request, render_template
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
    kanji_list = []
    for row in rows:
        result_string += row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3]
        kanji_list.append(row[0])

    return render_template('kanji_list.html',
                           k_list=kanji_list,
                           u_level=level,
                           u_selection=selection
                          )


@APP.route('/<selection>/<level>/<kanji>', methods=['POST', 'GET'])
def db_kanji(selection=None, level=None, kanji=None):
    """ Category page, displays a particular grade or JLPT level. """

    if request.method == 'POST':
        selection = request.form.split(' ')[0]
        level = request.form.split(' ')[1]
        kanji = request.form.split(' ')[2]

    kanji_query = """SELECT kanj, von, vkun, transl FROM info WHERE kanj = '%s'""" % kanji
    res_string = get_results(kanji_query)

    list_query = 'SELECT kanj FROM info WHERE %s = %s' % (selection, level)
    kanji_string = get_results(list_query)

    kanji_list = [l for l in kanji_string]
    current_pos = kanji_list.index(res_string[0])

    try:
        next_kanji = kanji_list[current_pos + 1]
    except IndexError:
        next_kanji = kanji_list[0]

    try:
        prev_kanji = kanji_list[current_pos - 1]
    except IndexError:
        prev_kanji = kanji_list[-1]

    return render_template('flashcard.html',
                           res_string=res_string,
                           k_list=kanji_list,
                           u_level=level,
                           u_selection=selection,
                           p_kanji=prev_kanji,
                           n_kanji=next_kanji
                          )


def get_results(query):
    """ Get database results for supplied query. """

    conn = psycopg2.connect(database='kanji', user=os.environ.get('POSTGRESQL_USER'),\
                            host=os.environ.get('POSTGRESQL_SERVICE_HOST'),\
                            password=os.environ.get('POSTGRESQL_PASSWORD'))
    cur = conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()
    result_string = ""

    for row in rows:
        if len(row) == 4:
            result_string += row[0] + ", " + row[1] + ", " + row[2] + ", "  + row[3]
        else:
            result_string += row[0]

    return result_string


def split_space(string):
    """ For use with jinja2 filters. """
    return string.strip().split()


if __name__ == '__main__':
    APP.jinja_env.filters['split_space'] = split_space
    APP.run(host='0.0.0.0', port=8080, debug=True)
