SELECT title FROM movies JOIN stars AS b_stars ON movies.id=b_stars.movie_id JOIN stars AS j_stars ON movies.id=j_stars.movie_id JOIN people AS b_people ON b_stars.person_id=b_people.id JOIN people AS j_people ON j_stars.person_id=j_people.id WHERE b_people.name = 'Bradley Cooper' AND j_people
.name = 'Jennifer Lawrence';
