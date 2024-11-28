import sqlite3
import json

# Connecting the file with the database
conn = sqlite3.connect('../database_test.db')
cursor = conn.cursor()

# Read the json file
with open('../../static/assets/json files/questions_extract.json', 'r') as json_file:
    info = json.load(json_file)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        questions_id TEXT PRIMARY KEY,
        prompts_id TEXT,
        user_id TEXT,
        question TEXT NOT NULL,
        taxonomy_bloom TEXT,
        rtti TEXT,
        exported BOOLEAN,
        date_created TEXT DEFAULT CURRENT_TIMESTAMP,
        antwoord TEXT NOT NULL,
        vak TEXT,
        onderwijsniveau TEXT,
        leerjaar INTEGER,
        question_index INTEGER
    )
''')

# cursor.execute('''
#     ALTER TABLE questions ADD COLUMN antwoord TEXT;
# ''')
# cursor.execute('''
#     ALTER TABLE questions ADD COLUMN vak TEXT;
# ''')
# cursor.execute('''
#     ALTER TABLE questions ADD COLUMN onderwijsniveau TEXT;
# ''')
# cursor.execute('''
#     ALTER TABLE questions ADD COLUMN leerjaar INTEGER;
# ''')
# cursor.execute('''
#     ALTER TABLE questions ADD COLUMN question_index INTEGER;
# ''')

for entry in info:
    cursor.execute('''
    INSERT OR REPLACE INTO questions (questions_id, prompts_id, user_id, question, taxonomy_bloom, rtti, exported, date_created, antwoord, vak, onderwijsniveau, leerjaar, question_index)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry['question_id'],
        entry.get('prompts_id', ''),
        entry.get('user_id', None),
        entry['vraag'],
        entry.get('taxonomy_bloom', None),
        entry.get('rtti', None),
        entry.get('exported', None),
        entry.get('date_created', None),
        entry['antwoord'],
        entry['vak'],
        entry['onderwijsniveau'],
        entry['leerjaar'],
        entry['question_index'],
    ))

conn.commit()
conn.close()

print("Succesvol toegevoegd!")