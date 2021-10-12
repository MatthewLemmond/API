from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bson.errors as berrors
import socket, os

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://root:{os.environ.get('MONGODB_ROOT_PASSWORD')}@172.21.176.54:27017/dev?authSource=admin"
mongo = PyMongo(app)
db = mongo.db

@app.route("/movies")
def get_movies():
    data = []
    movies = db.movies.find()
    for movie in movies:
        item = {
            "id": str(movie.get("_id")),
            "title": movie.get("title"),
            "rating": movie.get("rating")
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
            "title": movie.get("title"),
            "rating": movie.get("rating")
        }
        data.append(item)
    return jsonify(
        data=data
    )

@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json(force=True)
    print(type(data))
    db.movies.insert_one({
        "title": data.get("title"),
        "rating": data.get("rating")
    })
    return jsonify(
        message=f"\'{data['title']}\' successfully added."
    )

@app.route("/movies/<id>", methods=["PUT"])
def update_rating(id):
    data = request.get_json(force=True) ["rating"]
    try:
        response = db.movies.update_one({"_id": ObjectId(id)},
            {"$set": {"rating": data
        }})
        if response.matched_count:
            message = f"Movie with ID: \'{id}\' successfully updated with a rating of {data}."
        else:
            message=f"Movie with ID: \'{id}\' not found."
    except berrors.InvalidId:
        message = f"ID: \'{id}\' is not a valid ID."
    return jsonify(
        message=message
    )

@app.route("/movies/<id>", methods=["DELETE"])
def delete_movie(id):
    res = db.movies.delete_one({'_id': ObjectId(id)})
    if res.deleted_count:
        message=f"Movie with ID: \'{id}\' successfully removed."
    else:
        message=f"Movie with ID: \'{id}\' not found."
    return jsonify(
        message=message
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)