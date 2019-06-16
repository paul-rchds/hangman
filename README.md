# Hangman

Simple hangman game that can be played via web or JSON API.


## Requirements

* Chooses a random word out of 6 words: [3dhubs, marvin, print, filament, order, layer]
* Display the spaces for the letters of the word (eg: '_ _ _ _ _' for 'order')
* The user can choose a letter and if that letter exists in the chosen word it should be
shown on the puzzle (eg: asks for 'r' and now it shows '_ r _ _ r' for 'order')
* The user can only ask 5 letters that don't exist in the word and then it's game overIf the
user wins, congratulate the user and save their high score (you are free to define what is
a “high score”)
* Provide a simple API for clients to play the game
* Provide an interface for users to play the game


## Implementation
* Class based views are used so code can easily be shared between API and HTML template views.
* Postgres database is used to store game state and high scores.


## Notes
* For convenience sake, secrets have been commited to git as environmental variables in dokcer-compose file. 
* Letters are case-insensitive.

## Endpoints
Appending '/api' to any endpoint will return JSON and also accept it for POST requests. For example `GET /game` will return
a rendered template and `GET /game/api/` will return JSON. 


* `GET /`               # Returns registration form.
* `POST /`              # Accepts `username` 
* `GET /game`           # Returns current state of game based on current user set in session cookie.
* `POST /game`          # Accepts `letter` parameter.
* `GET /reset`          # Resets the game for the current user.
* `GET /high-scores`    # Lists high scores.


## Stack
* Flask
* SQLAlchemy
* Pytest
* Postgres
* Bootstrap
* Docker


## Get Started
```bash
git clone git@github.com:paul-rchds/hangman.git
docker-compose up
# Browse to http://127.0.0.1:8080
```


## Tests
```
docker-compose up
docker ps # Get container_id
docker exec <container_id> pytest -v
```


## Possible improvements
* In hindsight the views could have been simpler if they only implemented a JSON API and some front-end code 
was used to submit forms and get data.
* I should have used migrations to track changes to the database.