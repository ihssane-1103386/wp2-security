import sqlite3
import json
from datetime import datetime

# Test van ChatGPT voor opdracht 6
conn = sqlite3.connect('database_test.db')  # Pas de bestandsnaam aan naar jouw database
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        questions_id TEXT PRIMARY KEY,
        question TEXT,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
''')

# 3. Open het JSON-bestand en laad de data
with open('questions_extract_test.json') as f:
    vragen = json.load(f)

for vraag in vragen:
    question_id = vraag['question_id']  # Haal het question_id uit het JSON-object
    vraag_tekst = vraag['vraag']  # Haal de vraagtekst uit het JSON-object

    cursor.execute('''
        INSERT INTO questions (questions_id, question)
        VALUES (?, ?)
    ''', (question_id, vraag_tekst))

conn.commit()
conn.close()

print("Vragen succesvol toegevoegd!")