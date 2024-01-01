from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, date, timedelta
import os

def creer_connexion():
    return sqlite3.connect('emploidutemps.db')

def obtenir_repertoire_travail():
    return os.getcwd()

def initialiser_base_de_donnees(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS taches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                contenu TEXT NOT NULL,
                date DATETIME,
                urgent BIT, 
                creation DATETIME DEFAULT CURRENT_TIMESTAMP  
            )
        ''')

class Tache:
    def __init__(self, id, titre, contenu, urgent, date, creation=None):
        self.id = id
        self.titre = titre
        self.contenu = contenu
        self.date = date
        self.urgent = urgent
        self.creation = creation or datetime.utcnow()


class GestionnaireTaches:
    def __init__(self, base_de_donnees):
        self.base_de_donnees = base_de_donnees
        self.taches = []


    def ajouter_tache(self, titre, contenu, date_str, heure_str, urgent):
        date_formattee = datetime.strptime(date_str + ' ' + heure_str, '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')
        date_saisie = datetime.strptime(date_str, '%Y-%m-%d').date()

        date_actuelle = date.today()

        if date_saisie < date_actuelle:
            raise ValueError("La date de l'événement ne peut pas être antérieure à la date actuelle.")

        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO taches (titre, contenu, date, urgent, creation) VALUES (?, ?, ?, ?, ?)',
                        (titre, contenu, date_formattee, urgent, datetime.utcnow()))

        self.taches = self.recuperer_taches()


    def supprimer_tache(self, tache_id):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM taches WHERE id = ?', (tache_id,))
        self.taches = self.recuperer_taches()

    def recuperer_taches(self):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titre, contenu, urgent, date, creation FROM taches ORDER BY date')
            return [Tache(*row) for row in cursor.fetchall()]

class ApplicationFlask:
    
    def __init__(self, base_de_donnees):
        self.app = Flask(__name__)
        self.app.secret_key = "key"
        self.gestionnaire_taches = GestionnaireTaches(base_de_donnees)
        self.gestionnaire_taches.taches = self.gestionnaire_taches.recuperer_taches()
        self.configurer_routes()
        
    def configurer_routes(self):
        self.app.route('/')(self.accueil)
        self.app.route('/ajouter_tache', methods=['POST'])(self.ajouter_tache)
        self.app.route('/supprimer_tache/<int:id>')(self.supprimer_tache)
        self.app.route('/trier_evenements', methods=['POST'])(self.trier_evenements)

    def accueil(self):
        taches = self.gestionnaire_taches.recuperer_taches()
        return render_template('accueil.html', taches=taches)

    def ajouter_tache(self):
        if request.method == 'POST':
            titre = request.form['titre']
            contenu = request.form['contenu']
            date_str = request.form['date']
            heure_str = request.form['heure']
            urgent = request.form.get('urgent', 0)

            date_actuelle = date.today()
            date_saisie = datetime.strptime(date_str, '%Y-%m-%d').date()

            if date_saisie >= date_actuelle:
                try:

                    self.gestionnaire_taches.ajouter_tache(titre, contenu, date_str, heure_str, urgent)
                    flash("Tâche ajoutée avec succès.")
                except ValueError as e:
                    flash("Mamamia")

        return redirect(url_for('accueil'))

    def supprimer_tache(self, id):
        self.gestionnaire_taches.supprimer_tache(id)
        return redirect(url_for('accueil'))
    

    def tri_rapide_par_nom(self, taches): #FONCTION RECURSIVE DE TRI
        
        if len(taches) <= 1:
            return taches
        else:
            pivot = taches[0]
            taches_inf = [tache for tache in taches[1:] if tache.titre < pivot.titre]
            taches_sup = [tache for tache in taches[1:] if tache.titre >= pivot.titre]
            return self.tri_rapide_par_nom(taches_inf) + [pivot] + self.tri_rapide_par_nom(taches_sup)


    def trier_evenements(self):
        critere_tri = request.form.get('tri')
        taches_triees = []

        if critere_tri == 'urgent':

            print(self.gestionnaire_taches.taches)

            
        elif critere_tri == 'nom':
            
            taches_triees = self.tri_rapide_par_nom(self.gestionnaire_taches.taches)
            
        elif critere_tri == 'date':
            taches_triees = sorted(self.gestionnaire_taches.taches, key=lambda x: x.creation)


        return render_template('accueil.html', taches=taches_triees)

    def demarrer(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    base_de_donnees = sqlite3.connect('emploidutemps.db', check_same_thread=False)
    initialiser_base_de_donnees(base_de_donnees)
    app_flask = ApplicationFlask(base_de_donnees)
    app_flask.demarrer()
