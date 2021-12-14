"""
Initialisation de notre projet de site web
Contenant le nécessaire avec le test de la connection à la bdd
Ainsi que le chargement du Site Web
"""
import web_site_with_flask
import bdd_settings
import sqlite3


class Main:
    """
    Chargement du Site Web
    """
    def __init__(self):
        web_site_with_flask.WebSite()


def print_hi(name):
    """
    Dire bonjour à l'utisateur qui utilisera ce script :D
    :param name:
    String
        Le nom de l'utilisateur
    """
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {}'.format(name))  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('Manel :D')
    bdd_settings.test_con()
    try:
        bdd_settings.create_item_table_and_put_csv_in_sql()
    except sqlite3.OperationalError:
        print("La table que vous essayer de créer existe déja")
    Main()
