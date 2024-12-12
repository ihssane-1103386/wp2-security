import sqlite3

conn = sqlite3.connect('databases/database_toetsvragen.db')
cursor = conn.cursor()

query = ("SELECT question, vak, date_created, taxonomy_bloom FROM questions WHERE 1=1")

count_query = ("SELECT COUNT(*) FROM questions WHERE 1=1")

cursor.execute("SELECT DISTINCT vak FROM questions")

def load_queries(path):
    queries = {}
    query_name = None
    parameters = []

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('-[') and line.endswith(']'):
                if query_name and parameters:
                    queries[query_name] = ' '.join(parameters)
                query_name = line[4:-1]
                parameters = []
            elif query_name:
                parameters.append(line)

        if query_name and parameters:
            queries[query_name] = ' '.join(parameters)

    return queries