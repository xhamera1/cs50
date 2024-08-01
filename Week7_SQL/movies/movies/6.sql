SELECT AVG(rating) as av_rating FROM ratings where movie_id IN (SELECT id FROM movies WHERE year=2012);
