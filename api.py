from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/movies', methods=['GET'])
def get_movies():
    query_source = request.args.get('source')
    query_movie = request.args.get('movie')
    if not query_source or not query_movie:
        movies = Movie.query.all()
        return jsonify([{"id":movie.id,"title":movie.title,"genre":movie.genre} for movie in movies])
    else:
        if(query_source == 'omdb'):
            query_type = request.args.get('type')
            url = f'https://www.omdbapi.com/?apikey=d4c6caa6&t={query_movie}&type={query_type}'
            headers = {
                "accept": "application/json"
            }
        elif query_source == 'tmdb':
            url = f'https://api.themoviedb.org/3/search/movie?query={query_movie}&include_adult=false&language=en-US&page=1'
            headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYmM0YTUzZjVlMTYyODY1ZDc4MWZkMDY2NDQyOGU5ZSIsIm5iZiI6MTcyNzA5NDEzMy4xNTkzNzEsInN1YiI6IjY2ZTgxZGQwMDUwZjE0ZTRmY2NmZjVjZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.In1HXLOyBCx4rm0rrjQCVLWHZ6Bmwua_jh0OyOQ1Mh0"
            }
        else:
            return jsonify({"error":"Fonte de pesquisa inválida"})
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error":"Falha ao buscar dados da API externa! Verifique sua conexão com a internet e tente novamente."}), 500

@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    return jsonify({"id":movie.id,"title":movie.title,"genre":movie.genre}) if movie else ('', 404)

@app.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], genre=data['genre'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"id":new_movie.id,"title":new_movie.title,"genre":new_movie.genre}), 201

@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
        return jsonify({"error":"movie not found"}), 404

    db.session.delete(movie)
    db.session.commit()
    return '', 204

@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
        return jsonify({"error":"movie not found"}), 404
    
    data = request.get_json()
    movie.title = data.get('title', movie.title)
    movie.genre = data.get('genre', movie.genre)

    db.session.commit()
    return jsonify({
        "id":movie.id,
        "title":movie.title,
        "genre":movie.genre
        })

if __name__ == '__main__':
    app.run(port=5000, debug=True)