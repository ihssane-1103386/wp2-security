import sqlite3

def verbinding_maken_database():
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    conn.row_factory = sqlite3.Row
    return conn

def prompts_ophalen():
    conn = verbinding_maken_database()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                        prompts.prompts_id, 
                        prompts.prompt, 
                        users.display_name AS user_display_name, 
                        prompts.questions_count, 
                        prompts.questions_correct
                      FROM prompts
                      JOIN users ON prompts.user_id = users.user_id''')
    prompts = cursor.fetchall()
    conn.close()
    return prompts

def prompt_details_ophalen(prompts_id):
    conn = verbinding_maken_database()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                        prompts.prompts_id, 
                        prompts.prompt, 
                        prompts.prompt_details, 
                        users.display_name AS user_display_name, 
                        prompts.questions_count, 
                        prompts.questions_correct, 
                        prompts.questions_incorrect, 
                        prompts.date_created
                      FROM prompts
                      JOIN users ON prompts.user_id = users.user_id
                      WHERE prompts.prompts_id = ?''', (prompts_id,))
    prompt = cursor.fetchone()
    conn.close()
    return prompt

def prompt_verwijderen(prompts_id):
    conn = verbinding_maken_database()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM prompts WHERE prompts_id = ?', (prompts_id,))
    conn.commit()
    conn.close()

def prompt_toevoegen(user_id, prompt, prompt_details):

    try:
        conn = verbinding_maken_database()
        cursor = conn.cursor()


        query = """
        INSERT INTO prompts (user_id, prompt, questions_count, questions_correct, prompt_details, questions_incorrect)
        VALUES (?, ?, 0, 0, ?, 0);
        """


        cursor.execute(query, (user_id, prompt, prompt_details))
        conn.commit()

    except Exception as e:
        print(f"Fout tijdens het toevoegen van een nieuwe prompt vanuit model_prompts: {e}")
        raise e

    finally:
        conn.close()




