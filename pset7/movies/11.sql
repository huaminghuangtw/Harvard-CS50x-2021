-- In 11.sql, write a SQL query to list the titles of the five highest rated movies (in order)
-- that Chadwick Boseman starred in, starting with the highest rated
SELECT title FROM movies
JOIN ratings ON movies.id = ratings.movie_id
JOIN stars ON movies.id = stars.movie_id
WHERE person_id IN (SELECT id FROM people WHERE name = "Chadwick Boseman")
ORDER BY rating DESC
LIMIT 5;