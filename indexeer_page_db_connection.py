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

def prompt_ophalen_op_id(prompt_id):
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                        prompts.prompts_id, 
                        prompts.prompt_details 
                      FROM prompts
                      WHERE prompts.prompts_id = ?''', (prompt_id,))
    prompt = cursor.fetchone()
    conn.close()
    return prompt

def prompt_question_count_verhogen(): #nog niet helemaal in werking
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE prompts set''')
