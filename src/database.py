import MySQLdb
import MySQLdb.cursors
import os
from flask import g
from flask import current_app as app
from werkzeug.local import LocalProxy


def connect_db():
    conn = MySQLdb.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        passwd=os.environ.get("MYSQL_PASSWORD"),
        db=os.environ.get("MYSQL_DATABASE"),
        cursorclass=MySQLdb.cursors.DictCursor,
    )

    # conn.autocommit(False)

    return conn


def get_db():
    """
    gets the database connection variable
    """
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = connect_db()

    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


db = LocalProxy(get_db)
