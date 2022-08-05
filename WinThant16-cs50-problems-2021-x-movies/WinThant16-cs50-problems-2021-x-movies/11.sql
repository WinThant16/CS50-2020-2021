SELECT movies.title FROM movies
JOIN stars ON movies.id=stars.movie_id
JOIN ratings ON ratings.movie_id=movies.id
JOIN people ON people.id=stars.person_id
WHERE people.name ="Chadwick Boseman"
ORDER BY ratings.rating DESC LIMIT 5;