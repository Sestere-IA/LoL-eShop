import sqlite3
import sys


def test_con():
    con = sqlite3.connect("database/lol_item.db")
    if con:
        print("Connection Successful!")
    else:
        print("Connection Failed!")
        sys.exit()


def create_table_lol_items():
    con = sqlite3.connect("database/lol_item.db")
    cursor = con.cursor()

    sql_file = open("requete_sql/create_table_lol_item.sql")
    sql_as_string = sql_file.read()

    cursor.executescript(sql_as_string)


def connect_db():
    sql = sqlite3.connect('University.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
