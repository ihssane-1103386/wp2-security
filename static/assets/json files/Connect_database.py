import sqlite3
import json

# Connecting the file with the database
conn = sqlite3.connect('database_test.db')
cursor = conn.cursor()

# Read the json file
with open('questions_extract_test.json', 'r') as json_file:
    info = json.load(json_file)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        questions_id TEXT PRIMARY KEY,
        prompt_id TEXT,
        user_id TEXT,
        question TEXT NOT NULL,
        taxonomy_bloom TEXT,
        rtti TEXT,
        exported BOOLEAN,
        datum_created TEXT DEFAULT CURRENT_TIMESTAMP,
        antwoord TEXT NOT NULL,
        vak TEXT,
        onderwijsniveau TEXT,
        leerjaar INTEGER,
        question_index INTEGER
    )
''')

for entry in info:
    cursor.execute('''
    INSERT OR REPLACE INTO questions (questions_id, prompt_id, user_id, question, taxonomy_bloom, antwoord, vak, onderwijsniveau, leerjaar, question_index, datum)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry['question_id'],
        entry['vraag'],
        entry['antwoord'],
        entry['vak'],
        entry['onderwijsniveau'],
        entry['leerjaar'],
        entry['question_index'],
        entry.get('datum')
    ))

conn.commit()
conn.close()

print("Succesvol toegevoegd!")