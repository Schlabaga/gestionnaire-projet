# main.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def creer_connexion():
    return sqlite3.connect('emploidutemps.db')

def initialiser_base_de_donnees(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS taches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                contenu TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

class Tache:
    
    def __init__(self, id, titre, contenu, date=None):
        self.id = id
        self.titre = titre
        self.contenu = contenu
        self.date = date or datetime.utcnow()

    def __str__(self):
        return f"Tâche {self.titre} ({self.date})"


class GestionnaireTaches:
    
    def __init__(self, base_de_donnees):
        self.base_de_donnees = base_de_donnees

    def ajouter_tache(self, titre, contenu):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO taches (titre, contenu) VALUES (?, ?)', (titre, contenu))

    def supprimer_tache(self, tache_id):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM taches WHERE id = ?', (tache_id,))

    def recuperer_taches(self):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titre, contenu, date FROM taches ORDER BY date')
            return [Tache(*row) for row in cursor.fetchall()]


class ApplicationFlask:
    
    def __init__(self, base_de_donnees):
        self.app = Flask(__name__)
        self.gestionnaire_taches = GestionnaireTaches(base_de_donnees)
        self.configurer_routes()

    def configurer_routes(self):
        self.app.route('/')(self.accueil)
        self.app.route('/ajouter_tache', methods=['POST'])(self.ajouter_tache)
        self.app.route('/supprimer_tache/<int:id>')(self.supprimer_tache)

    def accueil(self):
        taches = self.gestionnaire_taches.recuperer_taches()
        return render_template('accueil.html', taches=taches)

    def ajouter_tache(self):
        if request.method == 'POST':
            titre = request.form['titre']
            contenu = request.form['contenu']
            self.gestionnaire_taches.ajouter_tache(titre, contenu)
        return redirect(url_for('accueil'))

    def supprimer_tache(self, id):
        self.gestionnaire_taches.supprimer_tache(id)
        return redirect(url_for('accueil'))

    def demarrer(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    base_de_donnees = sqlite3.connect('emploidutemps.db', check_same_thread=False)
    initialiser_base_de_donnees(base_de_donnees)
    
    app_flask = ApplicationFlask(base_de_donnees)
    app_flask.demarrer()
