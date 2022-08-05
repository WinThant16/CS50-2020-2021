SELECT people.name FROM people
JOIN stars ON stars.person_id=people.id
WHERE people.id IN
(SELECT DISTINCT stars.person_id FROM stars
JOIN movies ON movies.id=stars.movie_id
WHERE movies.year="2004")
ORDER BY people.birth;