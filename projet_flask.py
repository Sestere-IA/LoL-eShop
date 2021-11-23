from flask import Flask, request, url_for, redirect, render_template, g, session
import gestion_bdd


class FlaskUse:

    def __init__(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Myscretkey'
        app.config['PERMANENT_SESSION_LIFETIME'] = 10

        # teardown_X() closes or otherwise deallocates the resource if it exists.
        # It is registered as a teardown_appcontext() handler.
        @app.teardown_appcontext
        def close_db(error):
            if hasattr(g, 'sqlite_db'):
                g.sqlite_db.close()

        @app.route('/')
        def index():
            return redirect(url_for('home'))

        @app.route('/home', methods=['GET', 'POST'])
        def home():
            if request.method == "GET":
                if 'pseudo' in session:
                    identifier_vous = ""
                    pseudo = session['pseudo']
                    href1_message = "Ajouter un nouvel étudiant"
                    href2_message = "Afficher la liste des étudiants"
                    href3_message = "Supprimer un étudiant"
                    connection = pseudo

                else:

                    identifier_vous = "Identifiez-vous"
                    pseudo = ""
                    href1_message = ""
                    href2_message = ""
                    href3_message = ""
                    connection = "Connection"

                return render_template("home.html",
                                       identifier_vous=identifier_vous,
                                       pseudo=pseudo, href1_message=href1_message,
                                       connection=connection,
                                       href2_message=href2_message,
                                       href3_message=href3_message)
            else:
                pseudo = request.form['name']
                session['pseudo'] = pseudo
                if 'pseudo' in session:
                    message_visit = "C'est un plaisir de se revoir, {pseudo} !" \
                        .format(pseudo=session['pseudo'])
                    identifier_vous = "Déconnectez-vous"
                    href1_message = "Ajouter un nouvel étudiant"
                    href2_message = "Afficher la liste des étudiants"
                    href3_message = "Supprimer un étudiant"
                    connection = pseudo

                else:
                    message_visit = "Bonjour, c'est votre première visite ?"
                    identifier_vous = "Identifiez-vous"
                    href1_message = ""
                    href2_message = ""
                    href3_message = ""
                    connection = "Connection"

                return render_template("home.html",
                                       msg=message_visit,
                                       identifier_vous=identifier_vous,
                                       pseudo=pseudo, href1_message=href1_message,
                                       href2_message=href2_message,
                                       connection=connection,
                                       href3_message=href3_message)

        @app.route('/pseudo', methods=['GET', 'POST'])
        def get_pseudo():
            if request.method == "GET":
                if "pseudo" in session:
                    message_visit = "Bonjour, c'est votre première visite ?"
                    identifier_vous = "Identifiez-vous"
                    pseudo = ""
                    session.pop('pseudo', None)
                    return render_template("home.html", msg=message_visit,
                                           identifier_vous=identifier_vous,
                                           pseudo=pseudo, connection="Connection")

                else:
                    return render_template("page_get_pseudo.html",
                                           msg_get_speudo="Connection", connection="Connection")
            else:
                pass

        @app.route('/newpseudo', methods=['GET', 'POST'])
        def get_new_pseudo():
            if request.method == "POST":
                return render_template("new_visitor.html")
            else:
                pass

        @app.route('/coin')
        def coin():
            if "pseudo" in session:
                return render_template("coin.html", connection="Connection")
            else:
                return render_template("connect_before_get_coin.html")

        @app.route('/display', methods=['POST', 'GET'])
        def viewresults():
            if "pseudo" in session:
                pseudo = session['pseudo']
            else:
                pseudo = ""
            db = gestion_bdd.get_db()
            cur = db.execute('select * from etudiant_table')
            results = cur.fetchall()

            return render_template("view.html", rows=results, pseudo=pseudo)

        @app.route('/add', methods=['POST', 'GET'])
        def add():
            if "pseudo" in session:
                pseudo = session['pseudo']
            else:
                pseudo = ""
            if request.method == 'GET':
                return render_template('add.html')
            else:
                # Ajouter un nouvel utilisateur via le formulaire de la page
                name = request.form['name']
                surname = request.form['surname']
                level = request.form['level']
                mail = request.form['mail']
                adresse = request.form['adresse']
                print(name, surname, level, mail, adresse)

                db = gestion_bdd.get_db()
                db.execute(
                    'insert into etudiant_table (etudiant_name, etudiant_surname, etudiant_level, etudiant_mail, '
                    'etudiant_adresse) values (?, ?, ?, ?, ?)', [name, surname, level, mail, adresse])
                db.commit()

                return redirect(url_for('viewresults', name=name, surname=surname, pseudo=pseudo))

        @app.route('/delete', methods=['POST', 'GET'])
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

                return render_template("delete.html", rows=results, pseudo=pseudo)

        app.run()
