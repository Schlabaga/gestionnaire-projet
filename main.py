from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def creer_connexion():
    return sqlite3.connect('emploidutemps.db')

def initialiser_base_de_donnees():
    conn = creer_connexion()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS taches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                contenu TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/')
def accueil():
    conn = creer_connexion()
    with conn:
        cursor = conn.execute('SELECT * FROM taches ORDER BY date')
        taches = cursor.fetchall()
    return render_template('accueil.html', taches=taches)

@app.route('/ajouter_tache', methods=['POST'])
def ajouter_tache():
    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']
        conn = creer_connexion()
        with conn:
            conn.execute('INSERT INTO taches (titre, contenu) VALUES (?, ?)', (titre, contenu))
    return redirect(url_for('accueil'))


@app.route('/supprimer_tache/<int:id>')
def supprimer_tache(id):
    conn = creer_connexion()
    with conn:
        conn.execute('DELETE FROM taches WHERE id = ?', (id,))
    return redirect(url_for('accueil'))




if __name__ == '__main__':
    initialiser_base_de_donnees()
    app.run(debug=True)
