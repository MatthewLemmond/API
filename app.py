from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dev"
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(message=f"Welcome to my Movie app running from {hostname}.")

@app.route("/movies")
def get_movies():
    data = []
    movies = db.movies.find()
    for movie in movies:
        item = {
            "id": str(movie.get("_id")),
            "title": movie.get("title"),
            # "rating": movie.get(rating, default="None")
        }
        data.append(item)
    return jsonify(
        data=data
    )

@app.route("/movies/<title>")
def get_movie(title):
    data = []
    movies = db.movies.find({'title': title})
    for movie in movies:
        item = {
            "id": str(movie.get("_id")),
            "title": movie.get("title")
        }
        data.append(item)
    return jsonify(
        data=data
    )

@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json(force=True)
    db.movies.insert_one({"title": data["title"]})
    return jsonify(
        message=f"\'{data['title']}\' successfully added."
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)