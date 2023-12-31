import sqlite3
from tkinter import Tk, Label, Button, Entry, Listbox, END
from tkcalendar import DateEntry  
from datetime import datetime, date


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


class GestionnaireTaches:
    def __init__(self, base_de_donnees):
        self.base_de_donnees = base_de_donnees
        self.taches = []

    def ajouter_tache(self, titre, contenu, date_str):
        date_formattee = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')

        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO taches (titre, contenu, date) VALUES (?, ?, ?)', (titre, contenu, date_formattee))

        self.taches = self.recuperer_taches()

    def supprimer_tache(self, tache_id):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM taches WHERE id = ?', (tache_id,))

        self.taches = self.recuperer_taches()

    def recuperer_taches(self):
        with self.base_de_donnees as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titre, contenu, date FROM taches ORDER BY date')
            return [Tache(*row) for row in cursor.fetchall()]


class ApplicationTkinter:
    
    def __init__(self, base_de_donnees):
        self.base_de_donnees = base_de_donnees
        self.gestionnaire_taches = GestionnaireTaches(base_de_donnees)
        self.init_ui()

    def init_ui(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.title("Emploi du Temps")

        self.label_titre = Label(self.root, text="Nouveau Titre:")
        self.label_titre.pack()

        self.entry_titre = Entry(self.root)
        self.entry_titre.pack()

        self.label_contenu = Label(self.root, text="Nouveau Contenu :")
        self.label_contenu.pack()

        self.entry_contenu = Entry(self.root)
        self.entry_contenu.pack()

        self.label_date = Label(self.root, text="Date :")
        self.date_picker = DateEntry(self.root, date_pattern="yyyy-mm-dd", locale='fr_FR')
        self.date_picker.pack()

        self.button_ajouter = Button(self.root, text="Ajouter", command=self.ajouter_tache)
        self.button_ajouter.pack()

        self.listbox_taches = Listbox(self.root)
        self.listbox_taches.pack()

        self.charger_taches()

        self.root.mainloop()

    def ajouter_tache(self):
        
        titre = self.entry_titre.get()
        contenu = self.entry_contenu.get()
        date_str = str(self.date_picker.get())

        date_actuelle = date.today().strftime('%Y-%m-%d')
        date_saisie = datetime.strptime(date_str, '%Y-%m-%d').date()

        if date_saisie >= date.today() or (titre or contenu != ""):
            if titre != "":
                self.gestionnaire_taches.ajouter_tache(titre, contenu, date_str)
                self.charger_taches()

    def charger_taches(self):
        self.listbox_taches.delete(0, END)
        taches = self.gestionnaire_taches.recuperer_taches()
        for tache in taches:
            self.listbox_taches.insert(END, f"{tache.titre} - {tache.contenu} - {tache.date}")


if __name__ == '__main__':
    base_de_donnees = sqlite3.connect('emploidutemps.db', check_same_thread=False)
    initialiser_base_de_donnees(base_de_donnees)

    app_tkinter = ApplicationTkinter(base_de_donnees)
