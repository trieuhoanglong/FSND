#FSND Project - Casting Agency
Heroku Link: https://rocky-plains-11114.herokuapp.com/

Local Run: http://127.0.0.1:5000

This project running in Python 3.10.6

Virtual Env: Please download Python 3.10.6 and create venv for this version

pip install -r requirements.txt:
This will install all the required packages.

####Key dependency:
- Flask - a lightweight backend microservices framework. Flask required to handle requests and responses.
- SQLAlchemy - Famous ORM to handle sqlite database
- Python Jose - For decode JWT token

To run the server, replace the DATABASE_URL value in setup.sh and run command:

`source setup.sh`

`flask run --reload`

Using the --reload flag will detect file changes and restart the server automatically.

##Application information

###Motivation
This application was inspired by Audacity, the goal of this application is to understand all the flow from setting up the database, define routing, authenciation / authorization to have permission in application's action, and to build it to the server up and running

For mentor: I don't have time to make an application for my own, and to build a nice front-end side to interact with the backend, but my goal here is done :), i'm a 6 years experience front-end developer with all famous framework: React, Vue and Angular. Thanks to Udacity, now i'm proud to say that I am a fullstack developer. Now i know how the backend side work, how to work with the cloud and much more things. I will keep continue my learning to archive more, thank you for all the lessions!

###Overview
Authentication: This application requires authentication to perform actions. All the endpoints require permissions, except the homepage endpoint, this endpoint is to check if the application is running.

The application has three different types of roles:

Casting Assistant:
- Can view actors and movies

Casting Director:
- All permissions a Casting Assistant has and… 
- Add or delete an actor from the database
- Modify actors or movies

Executive Producer:
- All permissions a Casting Director has and…
- Add or delete a movie from the database

###Error Handling
Errors will return as JSON

The API will return the following errors based on how the request fails:

400: Bad Request\
401: Unauthorized\
403: Forbidden\
404: Not Found\
405: Method Not Allowed\
422: Unprocessable Entity\
500: Internal Server Error\
###Endpoints
`GET /actors`: gets the list of all the actors; requires get:actors permission

Request: https://rocky-plains-11114.herokuapp.com/actors \
Response: [
{
"date_of_birth": "April 09, 1991",
"id": 1,
"name": "David Johnson"
}
]

`GET /actors/<actor_id>`: gets the actor information, also can view the list of movies that actor join in;
requires get:actors permission

Request: https://rocky-plains-11114.herokuapp.com/actors/1 \
Response: {
"date_of_birth": "April 09, 1991",
"id": 1,
"movies": [
"Titanic"
],
"name": "David Johnson"
},

`POST /actors`: adds new actor in the database; requires post:actor permission

Request: https://rocky-plains-11114.herokuapp.com/actors \
Payload:{
"name": "Andree Right",
"date_of_birth": "Jan 21, 1989"
}\
Response: {
"created_actor_id": 2,
"success": true
}

`PATCH /actors/<actor_id>`: Modify actor information; requires patch:actor permission

Request: https://rocky-plains-11114.herokuapp.com/actors/1 \
Payload:{
"date_of_birth": "Jan 21, 1990"
}\
Response: {
"date_of_birth": "January 21, 1990",
"id": 2,
"name": "Andree Right"
}

`DELETE /actors/<actor_id>`: Remove actor from the database; requires delete:actor permission

Request: https://rocky-plains-11114.herokuapp.com/actors/1 \
Response: {
"deleted_actor_id": 1,
"success": true
}

-------

`GET /movies`: gets the list of all the movies; requires get:movies permission

Request: https://rocky-plains-11114.herokuapp.com/movies \
Response: [
{
"id": 1,
"release_date": "January 21, 1989",
"title": "Titanic"
}
]

`GET /movies/<movie_id>`: gets the movie information, also can view the list of actors join in the movie;
requires get:movies permission

Request: https://rocky-plains-11114.herokuapp.com/movies/1 \
Response: {
"cast": [
"David Johnson"
],
"id": 1,
"imdb_rating": 4.4,
"release_date": "January 21, 1989",
"title": "Titanic"
},

`POST /movies`: adds new movie in the database; requires post:movie permission

Request: https://rocky-plains-11114.herokuapp.com/movies \
Payload: {
"title": "Titanic",
"release_date": "Jan 21, 1989",
"imdb_rating": 9,
"cast": ["Andree Right"]
}\
Response: {
"created_movie_id": 2,
"success": true
}

`PATCH /movies/<movie_id>`: Modify movie information; requires patch:movie permission

Request: https://rocky-plains-11114.herokuapp.com/movies/1 \
Payload: {
"imdb_rating": 6.5
}\
Response: {
"id": 1,
"imdb_rating": 6.5,
"release_date": "January 21, 1989",
"title": "Titanic"
}

`DELETE /movies/<movie_id>`: Remove actor from the database; requires delete:movie permission

Request: https://rocky-plains-11114.herokuapp.com/movies/1 \
Response: {
"deleted_movie_id": 1,
"success": true
}

###Testing
Before run the test, please change the DATABASE_URL in the setup.sh to point to your test_db, after that you need to run the setup.sh file by command: `source setup.sh` to set all the role's token to os.environ, after that, you need to run:

`dropdb fsnd_test` \
`createdb fsnd_test` \
`psql fsnd_test < fsnd_test.sql` \
`python test.py`
