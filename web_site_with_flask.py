"""
Gestion des pages, des chemins et des interraction de notre site web

"""
import flask
from flask import Flask, request, url_for, redirect, render_template, session

import bdd_settings


def all_info_for_navi_bar():
    """
    Recupérer les informations utile lié à la session
    :return
    Multiple value
        Info session
    """
    try:
        panier_len = session['panier_len']
        in_panier = session['in_panier_id']
        gold = " : " + str(session['gold'])
        total_price = session["total_price_panier"]
        return panier_len, in_panier, gold, total_price
    except KeyError:
        # no session
        session['panier_len'] = 0
        session['in_panier_id'] = []
        session["gold"] = 0
        session["total_price_panier"] = 0
        panier_len = session['panier_len']
        in_panier = session['in_panier_id']
        gold = " : " + str(session['gold'])
        total_price = session["total_price_panier"]
        return panier_len, in_panier, gold, total_price


class WebSite:
    """
    Gestion des pages, des chemins et des interraction de notre site web

    """

    def __init__(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Myscretkey'
        app.config['PERMANENT_SESSION_LIFETIME'] = 3600

        @app.route('/')
        def index():
            """
            Init basic route to redirect to /home
            :return
            Page
                Home page
            """
            return redirect(url_for('home'))

        @app.route('/clear_panier')
        def clear_panier():
            """
            Only use to clear cart
            :return
            Page
                Home page
            """
            session['panier_len'] = 0
            session['in_panier_id'] = []
            session["total_price_panier"] = 0
            return redirect(url_for('home'))

        @app.route('/del_elem', methods=['GET', 'POST'])
        def del_elem_in_cart():
            """
            Only use to del element in cart into panier page
            :return
            Page
                panier page
            """
            _id = request.form['code']
            for i, item in enumerate(session["in_panier_id"]):
                if _id in item:
                    session["total_price_panier"] -= int(item[3])
                    del session['in_panier_id'][i]
                    session['panier_len'] -= 1

            return redirect(url_for('panier'))

        @app.route('/panier', methods=['GET', 'POST'])
        def panier():
            """
            Gestion de la page panier

            :return:
            """
            panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
            connection = "Connection"
            if request.method == "GET":
                if 'pseudo' in session:
                    pseudo = session['pseudo']
                    connection = pseudo
            else:
                _id = request.form['code']
                id_item = bdd_settings.get_id_of_item_to_panier(_id)
                session["in_panier_id"].append(id_item)
                session["panier_len"] += 1
                session["total_price_panier"] += int(id_item[3])
                return redirect(url_for('home'))

            return render_template("panier.html",
                                   connection=connection,
                                   panier_len=panier_len,
                                   item_id_in_cart=in_panier,
                                   gold=gold,
                                   results=session["in_panier_id"],
                                   total_price=total_price)

        @app.route('/congrat', methods=['GET', 'POST'])
        def validation_paniner():
            """
            Afficher une page de félicitation après avoir valider le panier
            :return:
            """
            if 'pseudo' in session:
                if session['panier_len'] == 0:
                    print("Panier vide")
                    return redirect(url_for('panier'))
                else:
                    pseudo = session['pseudo']
                    panier_len, in_panier, gold, total_price = \
                        all_info_for_navi_bar()
                    if session['gold'] - total_price < 0:
                        print("Vous n'avez pas assez d'argent"
                              " sur votre compte")
                        return redirect(url_for('panier'))
                    else:
                        bdd_settings.validation_cart_del_money_to_bdd(pseudo,
                                                                      total_price)
                        session["gold"] -= total_price
                        return render_template("congrat_validation.html")
            else:
                return render_template(
                    "connect_to_account_to_validate_cart.html")

        @app.route('/home', methods=['GET', 'POST'])
        def home():
            """
            Afficher la page Home (page principal)
            :return
            page
                Home page
            """
            panier_len, in_panier, gold, total_price = \
                all_info_for_navi_bar()
            results = bdd_settings.see_bdd_item()
            if request.method == "GET":
                if 'pseudo' in session:
                    pseudo = session['pseudo']
                    connection = pseudo
                    if pseudo == "admin":
                        admin_suppresion_item = \
                            "Supprimer de la liste de vendre"
                        add_for_admin = "Ajouter un nouvel item"
                    else:
                        admin_suppresion_item = ""
                        add_for_admin = ""

                    identifier_vous = ""
                else:
                    identifier_vous = "Identifiez-vous"
                    pseudo = ""
                    add_for_admin = ""
                    connection = "Connection"
                    admin_suppresion_item = ""
                return render_template("home.html",
                                       identifier_vous=identifier_vous,
                                       pseudo=pseudo,
                                       add_for_admin=add_for_admin,
                                       connection=connection,
                                       results=results,
                                       admin_suppr_item=admin_suppresion_item,
                                       gold=gold, panier_len=panier_len)

        @app.route('/del_item_bdd', methods=['GET', 'POST'])
        def del_item_bdd_n_shop():
            """
            Supprimer un item du shop
            Seulement disponible si connecté avec un compte admin
            :return
            page
                Home page
            """
            _id = request.form['code']
            bdd_settings.del_item_in_bdd(_id)
            print("suppression de l'id {} dans la bdd".format(_id))
            return redirect(url_for('home'))

        @app.route('/add_item_admin', methods=['GET', 'POST'])
        def add_item_admin():
            """
            Ajouter un item dans le shop
            Seulement disponible si connecté avec un compte admin
            :return
            page
                Home page
            """
            if request.method == "GET":
                return render_template("add_item.html")
            else:
                item_id = request.form["id"]
                item_name = request.form["name"]
                item_explain = request.form["explain"]
                item_price = request.form["item_price"]
                item_sell_price = request.form["item_sell_price"]
                item_tag = request.form["tag"]
                item_image = request.form["image"]

                values_in_db = [item_id,
                                item_name,
                                item_explain,
                                item_price,
                                item_sell_price,
                                item_tag,
                                item_image]

                bdd_settings.add_item_in_bdd_admin(values_in_db)
                return redirect(url_for('home'))

        @app.route('/change_admin_status', methods=['GET', 'POST'])
        def change_admin_status():
            """
            Modifier le status d'un client
            Permet de rendre admin ou d'enlever le status admin d'un client
            :return
            page
                pseudo page
            """
            if "pseudo" in session:
                pseudo = session['pseudo']
                if pseudo == "admin":
                    _id = request.form['code']
                    if session['current_ID'] == int(_id):
                        print("Impossible de modifier son propre status")
                    else:
                        bdd_settings.change_admin_status_in_bdd(_id)
                        print("changement de status de l'id {} "
                              "client dans la bdd".format(_id))
                    return redirect(url_for('get_pseudo'))

        @app.route('/pseudo', methods=['GET', 'POST'])
        def get_pseudo():
            """
            Afficher la page de gestion de connection
            :return
            page
                pseudo page
            """
            panier_len, in_panier, gold, total_price = \
                all_info_for_navi_bar()
            result = ""
            table_hide = "hidden"
            if request.method == "GET":
                if "pseudo" in session:
                    pseudo = session["pseudo"]
                    if pseudo == "admin":
                        result = bdd_settings.see_bdd_client()
                        table_hide = ''
                    connection = pseudo

                    print("result: {}".format(result))
                    return render_template("setting_acoount.html",
                                           connection=connection,
                                           gold=gold,
                                           panier_len=panier_len,
                                           result=result,
                                           table_hide=table_hide)

                else:
                    return render_template("page_get_pseudo.html",
                                           msg_get_speudo="Connection",
                                           connection="Connection",
                                           panier_len=panier_len,
                                           gold=gold)
            else:
                if "pseudo" in session:
                    pseudo = session['pseudo']
                    if pseudo == "admin":
                        _id = request.form['code']
                        bdd_settings.del_client_in_bdd(_id)
                        print("suppression de l'id {} client dans la bdd"
                              .format(_id))
                        return redirect(url_for('get_pseudo'))
                else:

                    identifiant = request.form['identifiant']
                    password = request.form['mot_de_passe']
                    for identifiant_and_password_in_bdd in \
                            bdd_settings.check_identififiant_password_gold():
                        if identifiant == identifiant_and_password_in_bdd[0] \
                                and password == \
                                identifiant_and_password_in_bdd[1]:
                            print("Client dans la bdd autorasation"
                                  " de connection")
                            session['pseudo'] = identifiant

                            session['current_ID'] = \
                                bdd_settings.check_id_with_identifiant(
                                    identifiant)
                            gold_in_the_pocket = \
                                identifiant_and_password_in_bdd[2]
                            session['gold'] = gold_in_the_pocket
                            return redirect(url_for('home'))
                        else:
                            pass
                    print('Client pas dans la bdd, pas passer')
                    return render_template("page_get_pseudo.html",
                                           msg_get_speudo="Connection",
                                           connection="Connection",
                                           error_message="Info incorrect",
                                           gold=gold)

        @app.route('/coin', methods=['POST', 'GET'])
        def coin():
            """
            Afficher la page de gestion d'argent
            :return
            page
                coin page
            """
            panier_len, in_panier, gold, total_price = \
                all_info_for_navi_bar()
            if request.method == "GET":
                if "pseudo" in session:
                    pseudo = session['pseudo']
                    connection = pseudo
                    return render_template("coin.html",
                                           gold=gold,
                                           connection=connection,
                                           panier_len=panier_len)
                else:
                    return render_template("connect_before_get_coin.html")
            else:
                pseudo = session['pseudo']
                connection = pseudo
                secret_code = request.form['coin']
                validation_code_message = "Code incorrect," \
                                          " tu n'a pas le droit d'avoir " \
                                          "d'argent en plus"
                if secret_code == "motherload":
                    print("code valider")
                    validation_code_message = "BRAVO," \
                                              " c'est le bon code !" \
                                              " +10k in the bank"
                    bdd_settings.add_gold_in_the_pocket(pseudo)
                    session['gold'] += 10000
                return render_template("coin.html",
                                       gold=gold,
                                       connection=connection,
                                       validation_code_message=validation_code_message,
                                       panier_len=panier_len)

        @app.route('/newpseudo', methods=['GET', 'POST'])
        def get_new_pseudo():
            """
            Affichage de la page pour se creer un compte
            :return
            page
                new_visitor page
            """
            if request.method == "GET":
                error_message = ""
                return render_template("new_visitor.html",
                                       error_message=error_message)
            else:
                identifiant = request.form['identifiant']
                password = request.form['mot_de_passe']
                password_repeat = request.form['mot_de_passe_confirme']

                for identifiant_in_bdd in \
                        bdd_settings.check_identifiant_exist():

                    if identifiant_in_bdd[0] == identifiant:

                        error_message = "indentifiant deja dans la bdd"
                        return render_template("new_visitor.html",
                                               error_message=error_message)
                    else:
                        print("identificiant pas dans la base")

                if password == password_repeat:
                    bdd_settings.insert_client_in_bdd(identifiant,
                                                      password)
                    session['pseudo'] = identifiant
                    return redirect(url_for('home'))
                else:
                    error_message = "le mot de passe n'est pas le meme"
                    return render_template("new_visitor.html",
                                           error_message=error_message)

        @app.route('/disconnect')  # Access only for admin
        def disconnect():
            """
            Seulement utilisé pour déconnecter un client
            :return
            page
                Home page
            """
            session.pop("pseudo", None)
            session.pop("gold", None)
            return redirect(url_for('home'))

        app.run()
