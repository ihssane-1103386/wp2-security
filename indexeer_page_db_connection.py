import sqlite3


def prompt_lijst():
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()
    cursor = cursor.execute('''SELECT 
                            prompts.prompts_id, 
                            prompts.prompt
                            FROM prompts''')

    prompts= cursor.fetchall()
    conn.close()
    return prompts

