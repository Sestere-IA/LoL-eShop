import projet_flask
import gestion_bdd
import sqlite3


class Main:
    def __init__(self):
        projet_flask.FlaskUse()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('Manel :D')
    gestion_bdd.test_con()
    try:
        gestion_bdd.create_table_lol_items()
    except sqlite3.OperationalError:
        print("La table que vous essayer de créer existe déja")
    Main()
