from os import environ as env

from authlib.integrations.flask_client import OAuth
from dateutil.parser import parse
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth import requires_auth
from models import setup_db, Actor, Movie, db_drop_and_create_all

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def is_date(string):
    try:
        parse(string)
        return True

    except ValueError:
        return False


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = env.get("APP_SECRET_KEY")
    oauth = OAuth(app)
    setup_db(app)

    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

    # Uncomment for the first run to initial setup
    # db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def homepage():
        return jsonify({'status': 'Server is running!!'}), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors():
        actors_query = Actor.query.order_by(Actor.id).all()
        actors = [actor.long() for actor in actors_query]

        return jsonify({
            "success": True,
            "actors": actors
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth("get:actors")
    def get_actor_by_id(actor_id):
        actor = Actor.query.get_or_404(actor_id)

        return jsonify({
            "success": True,
            "actor": actor.full_info()
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def create_actor():
        try:
            request_body = request.get_json()
            if 'name' not in request_body or 'date_of_birth' not in request_body:
                raise KeyError

            if request_body['name'] == '' or is_date(request_body['date_of_birth']) is False:
                raise ValueError

            new_actor = Actor(request_body['name'],
                              request_body['date_of_birth'])
            new_actor.insert()

            return jsonify({
                "success": True,
                "created_actor_id": new_actor.id
            }), 201

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def update_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            request_body = request.get_json()
            if not bool(request_body):
                raise TypeError

            if "name" in request_body:
                if request_body["name"] == "":
                    raise ValueError

                actor.name = request_body["name"]

            if 'date_of_birth' in request_body:
                if request_body["date_of_birth"] == "":
                    raise ValueError

                actor.date_of_birth = request_body["date_of_birth"]

            actor.update()

            return jsonify({
                "success": True,
                "actor_info": actor.long()
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor_id": actor.id
            }), 200

        except Exception:
            abort(500)

    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies():
        movies_query = Movie.query.order_by(Movie.id).all()
        movies = [movie.short() for movie in movies_query]

        return jsonify({
            "success": True,
            "movies": movies
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth("get:movies")
    def get_movie_by_id(movie_id):
        movie = Movie.query.get_or_404(movie_id)

        return jsonify({
            "success": True,
            "movie": movie.full_info()
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def create_movie():
        try:
            request_body = request.get_json()
            print(request_body)
            if 'title' not in request_body \
                    or 'release_date' not in request_body \
                    or 'imdb_rating' not in request_body \
                    or 'cast' not in request_body:
                raise KeyError

            if request_body['title'] == '' \
                    or is_date(request_body['release_date']) is False \
                    or request_body['imdb_rating'] < 0 \
                    or request_body["imdb_rating"] > 10 \
                    or len(request_body["cast"]) == 0:
                raise TypeError
            new_movie = Movie(
                request_body['title'],
                request_body['release_date'],
                request_body['imdb_rating']
            )
            print(Actor)
            actors = Actor.query.filter(
                Actor.name.in_(request_body["cast"])).all()

            if len(request_body["cast"]) == len(actors):
                new_movie.cast = actors
                new_movie.insert()
            else:
                raise ValueError

            return jsonify({
                "success": True,
                "created_movie_id": new_movie.id
            }), 201

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def update_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            request_body = request.get_json()
            if not bool(request_body):
                raise TypeError

            if "title" in request_body:
                if request_body["title"] == "":
                    raise ValueError

                movie.title = request_body["title"]

            if "release_date" in request_body:
                if is_date(request_body["release_date"]) is False:
                    raise ValueError

                movie.release_date = request_body["release_date"]

            if "imdb_rating" in request_body:
                if request_body["imdb_rating"] < 0 \
                        or request_body["imdb_rating"] > 10:
                    raise ValueError

                movie.imdb_rating = request_body["imdb_rating"]

            if "cast" in request_body:
                if len(request_body["cast"]) == 0:
                    raise ValueError

                actors = Actor.query.filter(
                    Actor.name.in_(request_body["cast"])).all()

                if len(request_body["cast"]) == len(actors):
                    movie.cast = actors
                else:
                    raise ValueError

            movie.update()

            return jsonify({
                "success": True,
                "movie_info": movie.long()
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted_movie_id": movie.id
            }), 200

        except Exception:
            abort(500)

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(422)
    @app.errorhandler(500)
    def error_handler(error):
        if error.code == 422:
            error_content = "Please check your request, something is missing or is it incorrect."
        elif error.code == 401:
            error_content = "Please login to perform this action!"
        elif error.code == 403:
            error_content = "You do not have permission to perform this action!"
        elif error.code == 405:
            error_content = "Please check your endpoint again!"
        else:
            error_content = error.description
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error_content
        }), error.code

    return app


app = create_app()
