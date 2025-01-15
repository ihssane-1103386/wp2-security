import sqlite3


conn = sqlite3.connect('../../databases/database_toetsvragen.db')
cursor = conn.cursor()

cursor.execute('''
    ALTER TABLE questions ADD COLUMN bloom_answer TEXT;
''')

conn.commit()
conn.close()

print("De kolom is toegevoegd!")