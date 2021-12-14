""" Gestion de tout les elements lié à la base de données
"""

import sqlite3
import sys
import csv


def test_con():
    """Tester le connection avec la base de donnée
    Nous écrit si la connection a réussie ou non
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    if con:
        print("Connection Successful!")
    else:
        print("Connection Failed!")
        sys.exit()


def create_table_lol_items():
    """ Créer la table des items à vendre
    Utilise un fichier.sql pour faire cela"""

    con = sqlite3.connect("database/lol_e_shop.db")
    cursor = con.cursor()

    sql_file = open("requete_sql/create_table_lol_item.sql")
    sql_as_string = sql_file.read()

    cursor.executescript(sql_as_string)


def create_table_client():
    """ Creer la table des clients
    Utilise un fichier.sql pour faire cela
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    cursor = con.cursor()

    sql_file = open("requete_sql/create_table_client.sql")
    sql_as_string = sql_file.read()

    cursor.executescript(sql_as_string)


def create_item_table_and_put_csv_in_sql():
    """Création de la table des items à vendre
    Cette table est créer grace à un fichier csv.
    Celui-ci à été créé depuis du web scrapping
    ainsi que du nettoyage de données depuis
    Jupyter Notebook (tout dans le dossier
    de "jupyter_notebook".
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    try:

        cur.execute(
            "CREATE TABLE item_table "
            "(item_id, "
            "item_name, "
            "item_explain, "
            "item_buy_price, "
            "item_sell_price, "
            "item_tag, "
            "item_img_path);")  # Use your column

        with open('jupyter_notebook/item_with_img.csv', 'r') as fin:
            # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column
            # headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['item_id'],
                      i['name'],
                      i['explain'],
                      i['buy_price'],
                      i['sell_price'],
                      i['tag'],
                      i['path'])
                     for i in dr]

        cur.executemany(
            "INSERT INTO item_table "
            "(item_id,"
            " item_name,"
            " item_explain,"
            " item_buy_price,"
            " item_sell_price,"
            " item_tag,"
            "item_img_path)"
            " VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        con.close()

    except Exception as e:
        print(e)


def put_admin_on_bdd():
    """Ajout d'un admin dans la table client
    L'admin à des pouvoir supperrieur à un client normal
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("INSERT INTO client_table "
                "(client_identifiant, client_password, "
                "client_money, client_is_admin) VALUES (?, ?, ?, ?)",
                ["admin", "admin", 10000, True])
    con.commit()
    con.close()


def see_bdd_client():
    """ Afficher la base de donnée
    Le résultat peut être print en interne pour visualisé la table

    :return
    String
        Le résultat de la requête
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from client_table")
    result = cur.fetchall()
    # print(result)
    return result


def see_bdd_item():
    """ Afficher la base de donnée
    Le résultat est print en interne pour visualisé la table
    :return
    String
        Le résultat de la requête
    """

    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from item_table")
    result = cur.fetchall()
    print(result)
    return result


def drop_table():
    """
    Supprimer la table client de la base de données
    Uniquement utilisé en interne
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("drop table client_table")


def check_identifiant_exist():
    """
    Voir les différents identiant client dans la table client
    :return
    String
        Le resultat de la requête
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant from client_table")
    return cur.fetchall()


def check_identififiant_password_gold():
    """
    Voir les éléments clients dans la table clients
    :return
    String
        Résultat de la requête
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant,"
                " client_password,"
                " client_money"
                " from client_table")
    return cur.fetchall()


def check_id_with_identifiant(identifiant):
    """
    Voir l'ID du client dans la table client
    :param identifiant:
    String
        L'identifiant du client
    :return:
    String
        Le résultat de la requête
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_ID "
                "from client_table where client_identifiant=?",
                [identifiant])
    return cur.fetchone()[0]


def check_gold_in_the_pocket():
    """
    Vérifier l'argent de l'utilisateur dans la base de données
    :return
    String
        Le résultat de la requête
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_identifiant, client_password from client_table")
    return cur.fetchall()


def add_gold_in_the_pocket(identifiant):
    """
    Ajouter de l'argent à un client

    :param identifiant:
    String
        L'identifiant du client

    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("update client_table set client_money=client_money + ?"
                " where client_identifiant=?",
                (10000, identifiant))
    con.commit()
    con.close()


def get_id_of_item_to_panier(code):
    """
    Recupérer les informations d'un item
    :param code:
    Sring
        Le code de l'item
    :return:
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select * from item_table where item_id=?", [code])
    return cur.fetchone()


def validation_cart_del_money_to_bdd(identifiant, validation_cart):
    """
    Update l'argent du client après son achat
    :param identifiant:
    String
        L'identifiant du client
    :param validation_cart:
    int
        Le montant du panier validé
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("update client_table set client_money=client_money - ?"
                " where client_identifiant=?",
                (validation_cart, identifiant))
    con.commit()
    con.close()


def del_item_in_bdd(id_to_del):
    """
    Supprimer un item de la base de données
    :param id_to_del:
    int
        L'item a supprimer
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("delete from item_table where item_id=?", [id_to_del])
    con.commit()
    con.close()


def del_client_in_bdd(id_to_del):
    """
    Supprimer un client de la base de données
    :param id_to_del:
    int
        Le client a supprimer
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_is_admin from client_table where client_ID=?",
                [id_to_del])
    if int(cur.fetchone()[0]):  # if is admin cant del
        print("Impossible de supprimer un admin")
    else:
        cur.execute("delete from client_table where client_ID=?", [id_to_del])
        con.commit()
        con.close()


def insert_client_in_bdd(identifiant, password):
    """
    Insérer un nouveau client dans la base de donnée
    :param identifiant:
    String
        L'identifiant du client
    :param password:
    String
        Le mot de passe du client
    :return:
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute(
        'insert into client_table'
        ' (client_identifiant, client_password)'
        ' values (?, ?)', [identifiant, password])
    con.commit()
    con.close()


def change_admin_status_in_bdd(id_to_change):
    """
    Changer le status du client
    Permet de switch entre admin ou non
    :param id_to_change:
    int
        L'id du client à modifier
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select client_is_admin from client_table where client_ID=?",
                [id_to_change])
    if int(cur.fetchone()[0]):
        changement = False
    else:
        changement = True
    cur.execute("update client_table set client_is_admin=? where client_ID=?",
                [changement, id_to_change])
    con.commit()
    con.close()


def add_item_in_bdd_admin(values_to_add):
    """
    Ajouter un item de la base de données
    L'ajoute aussi dans le shop
    :param values_to_add:
    List[]
        La liste des valeurs à mettre dans chaque colonne
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("INSERT INTO item_table "
                "(item_id, item_name, item_explain,"
                " item_buy_price, item_sell_price, item_tag, "
                "item_img_path)"
                " VALUES (?, ?, ?, ?, ?, ?, ?);", values_to_add)
    con.commit()
    con.close()


def list_all_table():
    """
    Liste all tables in db
    :return
    String
        Le résultat de la requête
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("select name from sqlite_master where type='table';")
    return cur.fetchall()


def drop_specifi_table():
    """
    Supprimer une table dans la base de données
    """
    con = sqlite3.connect("database/lol_e_shop.db")
    cur = con.cursor()
    cur.execute("DROP TABLE item_table")
    con.commit()
    con.close()
