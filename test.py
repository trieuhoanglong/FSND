import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        # initialize app
        self.casting_assistant = os.environ.get('casting_assistant')
        self.casting_director = os.environ.get('casting_director')
        self.executive_producer = os.environ.get('executive_producer')
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # Define test variables
        self.new_actor = {
            "name": "David Johnson",
            "date_of_birth": "April 9, 1991"
        }

        self.invalid_new_actor = {
            "name": "David Johnson",
            "date_of_birth": "random string"
        }

        self.update_actor = {
            "name": "Andree Right Hand"
        }

        self.invalid_update_actor = {
            "date_of_birth": ""
        }

        self.new_movie = {
            "title": "Titanic",
            "release_date": "Jan 21, 1989",
            "imdb_rating": 9,
            "cast": ["David Johnson"]
        }

        self.invalid_new_movie = {
            "title": "Titanic",
            "release_date": "",
            "imdb_rating": 99,
            "cast": ["David Johnson"]
        }

        self.update_movie = {
            "imdb_rating": 4.4
        }

        self.invalid_update_movie = {
            "imdb_rating": 999
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)
        self.assertTrue(len(data["actors"]))

    def test_create_actor_with_casting_assistant(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        }, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_actor_id', data)

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.invalid_new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_info', data)

    def test_422_update_actor_info(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.invalid_update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_actors_by_id(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/3', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertTrue(len(data["actor"]["movies"]))

    def test_404_get_actors_by_id(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/999', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_casting_assistant(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_actor_with_executive_producer(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/2', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_actor_id', data)

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/999', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_movie_with_casting_director(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie_with_executive_producer(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        }, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_movie_id', data)

    def test_422_create_movie(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        }, json=self.invalid_new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info_with_executive_producer(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/2', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        }, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_info', data)
        self.assertEqual(data["movie_info"]["imdb_rating"],
                         self.update_movie["imdb_rating"])

    def test_422_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': f"Bearer {self.casting_director}"
        }, json=self.invalid_update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/2', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('imdb_rating', data['movie'])
        self.assertIn('cast', data['movie'])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_404_get_movie_by_id(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/999', headers={
            'Authorization': f"Bearer {self.casting_assistant}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_executive_producer(self):
        """Pass Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/1', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('success', data)

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/999', headers={
            'Authorization': f"Bearer {self.executive_producer}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
