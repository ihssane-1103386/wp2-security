-- Toetsvragen queries

-- [normal_query]
SELECT questions_id, question, vak, date_created, taxonomy_bloom FROM questions WHERE 1=1;

-- [count_query]
SELECT COUNT(*) FROM questions WHERE 1=1;

-- [vak_query]
SELECT DISTINCT vak FROM questions;

-- [fetch question for indexeren/taxonomie resultaat

-- [get_question]
SELECT question FROM questions WHERE questions_id = ?;

-- [get_vak]
SELECT vak FROM questions WHERE question_id = ?;

