-- Toetsvragen queries

-- [normal_query]
SELECT question, vak, date_created, taxonomy_bloom FROM questions WHERE 1=1

-- [count_query]
SELECT COUNT(*) FROM questions WHERE 1=1

-- [vak_query]
SELECT DISTINCT vak FROM questions