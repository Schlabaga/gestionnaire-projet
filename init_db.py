import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (title, content) VALUES (?, ?)",
            ('Premiere tâche', 'Content for the first post')
            )

cur.execute("INSERT INTO tasks (title, content) VALUES (?, ?)",
            ('Seconde tâche', 'Content for the second post')
            )

connection.commit()
connection.close()