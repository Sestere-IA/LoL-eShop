from flask import Flask, request, url_for, redirect, render_template, session
import gestion_bdd


class FlaskUse:

    def __init__(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Myscretkey'
        app.config['PERMANENT_SESSION_LIFETIME'] = 3600

        def all_info_for_navi_bar():
            try:
                panier_len = session['panier_len']
                in_panier = session['in_panier_id']
                gold = " : " + str(session['gold'])
                total_price = session["total_price_panier"]
                return panier_len, in_panier, gold, total_price
            except:
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

        @app.route('/')
        def index():
            return redirect(url_for('home'))

        @app.route('/clear_panier')
        def clear_panier():
            session['panier_len'] = 0
            session['in_panier_id'] = []
            session["total_price_panier"] = 0
            return redirect(url_for('home'))

        @app.route('/del_elem', methods=['GET', 'POST'])
        def del_elem_in_cart():
            _id = request.form['code']
            for i, item in enumerate(session["in_panier_id"]):
                if _id in item:
                    session["total_price_panier"] -= int(item[3])
                    del session['in_panier_id'][i]
                    session['panier_len'] -= 1

            return redirect(url_for('panier'))

        @app.route('/panier', methods=['GET', 'POST'])
        def panier():
            panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
            connection = "Connection"
            if request.method == "GET":
                if 'pseudo' in session:
                    pseudo = session['pseudo']
                    connection = pseudo
            else:
                _id = request.form['code']
                id_item = gestion_bdd.get_id_of_item_to_panier(_id)
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
            if 'pseudo' in session:
                pseudo = session['pseudo']
                panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
                gestion_bdd.validation_cart_del_money_to_bdd(pseudo, total_price)
                session["gold"] -= total_price
                return render_template("congrat_validation.html")
            else:
                return render_template("connect_to_account_to_validate_cart.html")

        @app.route('/home', methods=['GET', 'POST'])
        def home():
            panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
            db = gestion_bdd.get_db()
            cur = db.execute('select * from item_table')
            results = cur.fetchall()
            if request.method == "GET":
                if 'pseudo' in session:
                    pseudo = session['pseudo']
                    connection = pseudo
                    if pseudo == "admin":
                        admin_suppresion_item = "Supprimer de la liste de vendre"
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
                                       pseudo=pseudo, add_for_admin=add_for_admin,
                                       connection=connection, results=results,
                                       admin_suppr_item=admin_suppresion_item,
                                       gold=gold, panier_len=panier_len)

        @app.route('/del_item_bdd', methods=['GET', 'POST'])
        def del_item_bdd_n_shop():
            _id = request.form['code']
            gestion_bdd.del_item_in_bdd(_id)
            print("suppression de l'id {} dans la bdd".format(_id))
            return redirect(url_for('home'))

        @app.route('/add_item_admin', methods=['GET', 'POST'])
        def add_item_admin():
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

                gestion_bdd.add_item_in_bdd_admin(values_in_db)
                return redirect(url_for('home'))

        @app.route('/change_admin_status', methods=['GET', 'POST'])
        def change_admin_status():
            if "pseudo" in session:
                pseudo = session['pseudo']
                if pseudo == "admin":
                    _id = request.form['code']
                    if session['current_ID'] == int(_id):
                        print("Impossible de modifier son propre status")
                    else:
                        gestion_bdd.change_admin_status_in_bdd(_id)
                        print("changement de status de l'id {} client dans la bdd".format(_id))
                    return redirect(url_for('get_pseudo'))

        @app.route('/pseudo', methods=['GET', 'POST'])
        def get_pseudo():
            panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
            result = ""
            table_hide = "hidden"
            if request.method == "GET":
                if "pseudo" in session:
                    pseudo = session["pseudo"]
                    if pseudo == "admin":
                        result = gestion_bdd.see_bdd_client()
                        table_hide = ''
                    connection = pseudo

                    print("result: {}".format(result))
                    return render_template("setting_acoount.html", connection=connection, gold=gold,
                                           panier_len=panier_len, result=result, table_hide=table_hide)

                else:
                    return render_template("page_get_pseudo.html",
                                           msg_get_speudo="Connection", connection="Connection",
                                           panier_len=panier_len, gold=gold)
            else:
                if "pseudo" in session:
                    pseudo = session['pseudo']
                    if pseudo == "admin":
                        _id = request.form['code']
                        gestion_bdd.del_client_in_bdd(_id)
                        print("suppression de l'id {} client dans la bdd".format(_id))
                        return redirect(url_for('get_pseudo'))
                else:

                    identifiant = request.form['identifiant']
                    password = request.form['mot_de_passe']
                    for identifiant_and_password_in_bdd in gestion_bdd.check_identififiant_and_password_and_get_gold():
                        if identifiant == identifiant_and_password_in_bdd[0] \
                                and password == identifiant_and_password_in_bdd[1]:
                            print("Client dans la bdd autorasation de connection")
                            session['pseudo'] = identifiant

                            session['current_ID'] = gestion_bdd.check_id_with_identifiant(identifiant)
                            gold_in_the_pocket = identifiant_and_password_in_bdd[2]
                            session['gold'] = gold_in_the_pocket
                            return redirect(url_for('home'))
                        else:
                            pass
                    print('Client pas dans la bdd, pas passer')
                    return render_template("page_get_pseudo.html",
                                           msg_get_speudo="Connection",
                                           connection="Connection",
                                           error_message="Information incorrect",
                                           gold=gold)

        @app.route('/coin', methods=['POST', 'GET'])
        def coin():
            panier_len, in_panier, gold, total_price = all_info_for_navi_bar()
            if request.method == "GET":
                if "pseudo" in session:
                    pseudo = session['pseudo']
                    connection = pseudo
                    return render_template("coin.html", gold=gold, connection=connection,
                                           panier_len=panier_len)
                else:
                    return render_template("connect_before_get_coin.html")
            else:
                pseudo = session['pseudo']
                connection = pseudo
                secret_code = request.form['coin']
                validation_code_message = "Code incorrect, tu n'a pas le droit d'avoir d'argent en plus"
                if secret_code == "monsupercodesecret":
                    print("code valider")
                    validation_code_message = "BRAVO, c'est le bon code ! +10k in the bank"
                    gestion_bdd.add_gold_in_the_pocket(pseudo)
                    session['gold'] += 10000
                return render_template("coin.html", gold=gold,
                                       connection=connection,
                                       validation_code_message=validation_code_message,
                                       panier_len=panier_len)

        @app.route('/newpseudo', methods=['GET', 'POST'])
        def get_new_pseudo():
            if request.method == "GET":
                error_message = ""
                return render_template("new_visitor.html", error_message=error_message)
            else:
                identifiant = request.form['identifiant']
                password = request.form['mot_de_passe']
                password_repeat = request.form['mot_de_passe_confirme']

                for identifiant_in_bdd in gestion_bdd.check_identifiant_exist():

                    if identifiant_in_bdd[0] == identifiant:

                        error_message = "indentifiant deja dans la bdd"
                        return render_template("new_visitor.html", error_message=error_message)
                    else:
                        print("identificiant pas dans la base")

                if password == password_repeat:
                    db = gestion_bdd.get_db()
                    db.execute(
                        'insert into client_table (client_identifiant, client_password) values (?, ?)'
                        , [identifiant, password])
                    db.commit()
                    session['pseudo'] = identifiant
                    return redirect(url_for('home'))
                else:
                    error_message = "le mot de passe n'est pas le meme"
                    return render_template("new_visitor.html", error_message=error_message)

        """@app.route('/delete', methods=['POST', 'GET'])  # Access only for admin
        def delete_student():
            if "pseudo" in session:
                pseudo = session['pseudo']
            else:
                pseudo = ""
            if request.method == 'GET':
                db = gestion_bdd.get_db()
                cur = db.execute('select * from etudiant_table')
                results = cur.fetchall()

                return render_template("delete.html", rows=results)
            else:
                id_student = request.form['ID']

                db = gestion_bdd.get_db()
                db.execute('DELETE FROM etudiant_table WHERE etudiant_ID = ?',
                           [id_student])
                db.commit()

                db = gestion_bdd.get_db()
                cur = db.execute('select * from etudiant_table')
                results = cur.fetchall()

                return render_template("delete.html", rows=results, pseudo=pseudo)"""

        @app.route('/disconnect')  # Access only for admin
        def disconnect():
            session.pop("pseudo", None)
            session.pop("gold", None)
            return redirect(url_for('home'))

        app.run()
