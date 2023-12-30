from flask import Flask, render_template #LIBRAIRIE NECESSAIRE A LA 
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__, template_folder='templates')

print("test 2")
s
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks = tasks)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

print("blalab")

def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    if task is None:
        abort(404)
    return task


@app.route('/<int:task_id>')
def task(task_id):
    task = get_task(task_id)
    return render_template('task.html', task=task)

# 1. Ajoute une nouvelle tâche à la liste des tâches avec un titre, une description et une date d'échéance.
def add_task(title, description, due_date):
    pass

# 2. Supprime la tâche avec l'ID spécifié de la liste des tâches.
def delete_task(task_id):
    pass

# 3. Modifie les détails d'une tâche existante en utilisant son ID.
def update_task(task_id, title, description, due_date):
    pass

# 4. Renvoie les détails d'une tâche spécifique en fonction de son ID.
def get_task(task_id):
    pass

# 5. Renvoie la liste de toutes les tâches actuellement enregistrées.
def list_tasks():
    pass

# 6. Compte le nombre total de tâches dans la liste.
def count_tasks():
    pass

# 7. Renvoie une liste de tâches qui ont une date d'échéance égale à celle spécifiée.
def filter_tasks(due_date):
    pass

# 8. Marque une tâche comme complétée en utilisant son ID.
def mark_task_as_completed(task_id):
    pass

# 9. Renvoie une liste des tâches dont la date d'échéance est dépassée.
def find_task_echeance():
    pass

# 10. Vérifie récursivement si une tâche est complétée en vérifiant si toutes ses sous-tâches sont complétées.
def recursive_task_completion_check(task_id):
    pass

if __name__ == '__main__':
    app.run(debug=True)