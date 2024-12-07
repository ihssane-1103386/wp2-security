import sqlite3
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/", endpoint="toetsvragen")
def toetsvragen():
    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))

        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page

        cursor.execute("SELECT question, vak, date_created, taxonomy_bloom FROM questions LIMIT ? OFFSET ?", (per_page,start))
        question_page = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM questions")
        total_questions = cursor.fetchone()[0]
        total_pages = (total_questions + per_page - 1) // per_page

        next_page = page + 1 if end < total_questions else None
        prev_page = page - 1 if start > 0 else None

        show_first = page > 5
        show_last = page < total_questions - 5
        if total_pages <= 10:
            page_numbers = list(range(1, 11))
        else:
            if page <= 5:
                page_numbers = list(range(1, 6)) + ['...'] + [total_pages]
            elif page >= total_pages - 4:
                page_numbers = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
            else:
                page_numbers = [1, '...'] + list(range(page - 2, page + 3)) + ['...'] + [total_pages]

        return render_template('toetsvragen.html', vragen=question_page,
                               page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages, page_numbers=page_numbers, show_first=show_first, show_last=show_last)

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500

if __name__ == '__main__':
    app.run(debug=True)