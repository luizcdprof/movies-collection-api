from flask import Flask, jsonify, request

app = Flask(__name__)

movies = [
    {'id':1, 'title': 'Star Wars', 'genre': 'scifi'},
    {'id':2, 'title': 'It', 'genre': 'horror'},
    {'id':3, 'title': 'Um tira da pesada', 'genre': 'comedy'}
]

@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = next(
        (movie for movie in movies if movie['id'] == id),
        None
    )
    return jsonify(movie) if movie else ('', 404)

@app.route('/api/movies', methods=['POST'])
def add_movie():
    new_movie = request.get_json()
    movies.append(new_movie)
    return jsonify(new_movie), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)