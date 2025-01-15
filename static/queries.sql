-- Toetsvragen queries

-- [normal_query]
SELECT questions_id, question, vak, date_created, taxonomy_bloom FROM questions WHERE 1=1;

-- [count_query]
SELECT COUNT(*) FROM questions WHERE 1=1;

-- [vak_query]
SELECT DISTINCT vak FROM questions;

-- fetch question for indexeren/taxonomie resultaat

-- [get_question]
SELECT question FROM questions WHERE questions_id = ?;

-- [get_question_bloom_answer]
SELECT question, bloom_answer FROM questions WHERE questions_id = ?;

-- [get_vak]
SELECT vak FROM questions WHERE questions_id = ?;

-- [update_taxonomy]
UPDATE questions SET taxonomy_bloom = ? WHERE questions_id = ?;

-- [update_bloom_answer]
UPDATE questions SET bloom_answer = ? WHERE questions_id = ?;

-- [get_redacteur]
SELECT display_name, login, is_admin FROM users;

-- Fetch question, bloom_answer for wijzigen

-- [get_bloom_answer]
SELECT bloom_answer FROM questions WHERE questions_id = ?;

-- Nieuwe_redacteuren page

-- [get_redacteur]
INSERT INTO users (login, password, display_name, date_created, is_admin)
VALUES (?, ?, ?, ?, ?)