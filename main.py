from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Get the TMDB API key from the 'api_key' environment variable
api_key = os.environ.get("api_key")


def get_genre_list(api_key):
  url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data.get("genres", [])
  else:
    return []


def get_lead_cast_for_movie(api_key, movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    cast = data.get("cast", [])

    # Filter the cast to include only the lead actors/actresses (e.g., the first 3)
    lead_cast = [actor["name"] for actor in cast[:3]]
    return lead_cast
  else:
    return []


def get_movies_by_genre(api_key, genre_id):
  url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data.get("results", [])
  else:
    return []


# Existing functions for getting ratings and reviews...
def get_movie_ratings_and_reviews(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=videos,credits,reviews"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ratings = data.get("vote_average", 0)
        reviews = data.get("reviews", {}).get("results", [])[:2]  # Get the two most recent reviews
        return ratings, reviews
    else:
        return 0, []


@app.route('/')
def index():
  genres = get_genre_list(api_key)
  return render_template('index.html', genres=genres)


@app.route('/recommend', methods=['POST'])
def recommend():
    genre_id = request.form['genre']
    actor_name = request.form['actor']  # User-selected actor
    year = request.form['year']  # User-selected year
    
    movies = get_movies_by_genre(api_key, genre_id)
    
    # If an actor is selected, filter movies based on the actor
    if actor_name:
        actor_filtered_movies = []
        for movie in movies:
            cast = get_lead_cast_for_movie(api_key, movie["id"])  # Use lead cast
            if actor_name in cast:
                actor_filtered_movies.append(movie)
        movies = actor_filtered_movies
    
    # Fetch lead cast information for each movie and add it to the movie dictionary
    for movie in movies:
        movie['lead_cast'] = get_lead_cast_for_movie(api_key, movie['id'])
        movie['rating'], movie['reviews'] = get_movie_ratings_and_reviews(api_key, movie['id'])


# Existing code ...

    return render_template('recommendations.html',
                         movies=movies,
                         actor_name=actor_name)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
