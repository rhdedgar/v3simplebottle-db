import psycopg2
from bottle import route, run
import os



@route('/')
def index():
    all_buttons = (
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 1</button>\n'
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 2</button>\n'
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 3</button>\n'
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 4</button>\n'
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 5</button>\n'
    '<button type=\"button\" onclick=\"alert(\'Hello world!\')\">Grade 6</button>\n'
    )
    return all_buttons

@route('/db')
def dbexample():
    print os.environ.get('POSTGRESQL_USER')
    print "After Env"
    try:
        conn = psycopg2.connect(database='kanji',\
        user=os.environ.get('POSTGRESQL_USER'),\
        host=os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST'),\
        password=os.environ.get('POSTGRESQL_PASSWORD'))
    except:
        print os.environ.get('POSTGRESQL_USER') + "  " + \
        os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST')

    cur = conn.cursor()
    cur.execute("""SELECT kanj, von, vkun, transl from info
    WHERE school = '1'""")

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>"+ row[0]+ ", "+ row[1]+ row[2]+ row[3]+ "</h3>"

    return  result_string

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
