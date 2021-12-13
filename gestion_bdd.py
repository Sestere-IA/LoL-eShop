import sqlite3
import sys
import csv
from flask import g


def test_con():
    con = sqlite3.connect("database/lol_e_shop.db")
    if con:
        print("Connection Successful!")
    else:
        print("Connection Failed!")
        sys.exit()


def create_table_lol_items():
    con = sqlite3.connect("database/lol_e_shop.db")
    cursor = con.cursor()

    sql_file = open("requete_sql/create_table_lol_item.sql")
    sql_as_string = sql_file.read()

    cursor.executescript(sql_as_string)


def create_table_client():
    con = sqlite3.connect("database/lol_e_shop.db")
    cursor = con.cursor()

    sql_file = open("requete_sql/create_table_client.sql")
    sql_as_string = sql_file.read()

    cursor.executescript(sql_as_string)


def connect_db():
    sql = sqlite3.connect('database/lol_e_shop.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def put_csv_in_sql():  # Création de la db ainsi que de la table pour vendre ;D
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    try:

        cur.execute(
            "CREATE TABLE item_table (item_id, item_name, item_explain, item_buy_price, item_sell_price, item_tag, item_img_path);")  # use your column

        with open('jupyter_notebook/item_with_img.csv', 'r') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['item_id'], i['name'], i['explain'], i['buy_price'], i['sell_price'], i['tag'], i['path'])
                     for i in dr]

        cur.executemany(
            "INSERT INTO item_table "
            "(item_id, item_name, item_explain,"
            " item_buy_price, item_sell_price, item_tag, "
            "item_img_path)"
            " VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        con.close()

    except:
        pass


def put_admin_on_bdd():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("INSERT INTO client_table "
                "(client_identifiant, client_password, "
                "client_money, client_is_admin) VALUES (?, ?, ?, ?)",
                ["admin", "admin", 10000, True])
    con.commit()
    con.close()


def see_bdd_client():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from client_table")
    result = cur.fetchall()
    #print(result)
    return result


def see_bdd_item():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from item_table")
    print(cur.fetchall())


def drop_table():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("drop table client_table")


def check_identifiant_exist():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant from client_table")
    return cur.fetchall()


def check_identififiant_and_password_and_get_gold():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant, client_password, client_money from client_table")
    return cur.fetchall()


def check_id_with_identifiant(identifiant):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_ID from client_table where client_identifiant=?", [identifiant])
    return cur.fetchone()[0]


def check_gold_in_the_pocket():
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant, client_password from client_table")
    return cur.fetchall()


def add_gold_in_the_pocket(identifiant):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("update client_table set client_money=client_money + ? where client_identifiant=?",
                (10000, identifiant))
    con.commit()
    con.close()


def get_id_of_item_to_panier(code):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from item_table where item_id=?", [code])
    return cur.fetchone()


def validation_cart_del_money_to_bdd(identifiant, validation_cart):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("update client_table set client_money=client_money - ? where client_identifiant=?",
                (validation_cart, identifiant))
    con.commit()
    con.close()


def del_item_in_bdd(id_to_del):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("delete from item_table where item_id=?", [id_to_del])
    con.commit()
    con.close()


def del_client_in_bdd(id_to_del):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_is_admin from client_table where client_ID=?", [id_to_del])
    if int(cur.fetchone()[0]):  # if is admin cant del
        print("Impossible de supprimer un admin")
    else:
        cur.execute("delete from client_table where client_ID=?", [id_to_del])
        con.commit()
        con.close()


def change_admin_status_in_bdd(id_to_change):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_is_admin from client_table where client_ID=?", [id_to_change])
    if int(cur.fetchone()[0]):
        changement = False
    else:
        changement = True
    cur.execute("update client_table set client_is_admin=? where client_ID=?",
                [changement, id_to_change])
    con.commit()
    con.close()


def add_item_in_bdd_admin(values_to_add):
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("INSERT INTO item_table "
                "(item_id, item_name, item_explain,"
                " item_buy_price, item_sell_price, item_tag, "
                "item_img_path)"
                " VALUES (?, ?, ?, ?, ?, ?, ?);", values_to_add)
    con.commit()
    con.close()
