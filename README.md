## CAST! The Casting Agency App
CAST! is the name of this Casting Agency Application. The Executive Producer at CAST! had a major painpoint; that it was very difficult to trace which movie is assigned to which starring actor (and vice versa) and which showings have been confirmed alongside their respective details. As the lead software engineer, my main motivation for creating CAST! was to create a system to simplify and streamline the process of showcasing and accessing the details of movies, starring actors, and showings.

----------------------------------------------------------------------

### Table of Contents
1. [How to access CAST!](https://github.com/morangi2/CastingAgencyApp/blob/main/README.md#how-to-access-cast)
2. [CAST! V1](https://github.com/morangi2/CastingAgencyApp/blob/main/README.md#cast-v1)
3. [CAST! V2](https://github.com/morangi2/CastingAgencyApp/blob/main/README.md#cast-v2)
4. [To run the app locally for the first time](https://github.com/morangi2/CastingAgencyApp#to-run-the-app-locally-for-the-first-time)
5. [Tech Stack (Dependencies)](https://github.com/morangi2/CastingAgencyApp#tech-stack-dependencies)
6. [Main Files: Project Structure](https://github.com/morangi2/CastingAgencyApp#main-files-project-structure)
7. [Endpoints Documentation](https://github.com/morangi2/CastingAgencyApp#endpoints-documentation)
8. [Actors Endpoints](https://github.com/morangi2/CastingAgencyApp#actors-endpoints)
9. [Movies Endpoints](https://github.com/morangi2/CastingAgencyApp#movies-endpoints)
10. [Showings Endpoints](https://github.com/morangi2/CastingAgencyApp#showings-endpoints)
11. [Hosting on Heroku](https://github.com/morangi2/CastingAgencyApp#hosting-on-heroku-deplyment-via-cli-and-git)
12. [Continuous Deployment via GitHub]()
13. [Creating a new Heroku Postgres Database Mid-project]()
14. [Authentication with Auth0]()
15. [Authorization with Auth0](https://github.com/morangi2/CastingAgencyApp#authorization-with-auth0)
16. [Appreciation](https://github.com/morangi2/CastingAgencyApp/blob/main/README.md#appreciation)

----------------------------------------------------------------------


### How to access CAST!
- Public URL: https://castingagency-mjko-c1b260bbded2.herokuapp.com/
- **NOTE:** Accessing CAST! beyond the home-page requires authentication. Feel free to sign-up on the screen that shows up, and relevant roles will be granted within 24 hours.

### CAST! V1
This is what you currently see in this app, which incoporates 4 major functionalities;
1. Movies; posting a new movie, viewing a list of movies, viewing the details of a specific movie (including past and upcoming showings and if they are seeking casting opportunities), editing and deleting a specific movie.
2. Actors; posting a new starring actor, viewing a list of starring actors grouped by geographical location, viewing the details of a specific actor (including past and upcoming showings and if they are seeking casting opportunities), editing and deleting a starring actor.
3. Showings; posting a new showwing which highlights the movie that will be showed, alongside the starring actor, and the date and time of the showing.
4. Search movies & actors; ***

### CAST! V2
This will be the 2nd iteration of the app adding onto the functionality above as illustrated below;
1. Movies; add the details of the producers of the movie
2. Actors; include other actors (not just starring actors) and tag them accordingly
3. Showings; include the details of the cinemas (and locations) where the showing will take place, and tag more actors in a given showing.
4. Authentication; Provide a passwordless option for log in


------------------------------------

## To run the app locally for the first time:
1. **Download the project starter code locally**
```
git clone https://github.com/morangi2/CastingAgencyApp.git
cd ******/starter_code 
```
2. **Create an empty repository in your GitHub online account. Change the remote repo path in your local repo, using the following commands:**
```
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```
3. **Push your local repo into your GitHub account using the following commands:**
```
git add . --all   
git commit -m "your comment"
git push -u origin master
```
4. **Initialize and activate your virtual environment**
```
python3 -m venv myenv
source venv/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
``` 
5. **Install all the dependencies needed for this project:**
```
pip install -r requirements.txt
```
6. **Create the project database:**
```
createdb name_of_database
```
7. **Setup Migration to initialize your database schema:**
```
python3 manage.py db init # to initialize the migrations directory
python3 manage.py db migrate # details the model changes to be made with upgrade and downgrade logic setup
python3 manage.py db upgrade # to apply the migration
```
8. **Activate your environment variables in ```setup.sh```;**
```
chmod +x setup.sh
source setup.sh
```
>**Note** The shell script, ```setup.sh```, is not included in this repo as it contains a bunch of secret keys. You'll want to set this up for yourself locally in the format below:

_A. Basic Environment Variables_
```
#!/bin/bash
export DATABASE_URL="link_to_your_postgres_or_any_other_database"
export DATABASE_URL_TEST="link_to_your_test_database"
export SECRET_KEY='link_to_a_random_secret_key_to_use_on_your_config_file'
```
_B. Environment Variables if you are setting up authentication via Auth0_
```
export CALLBACK_URL='callback url here'
export AUTH0_DOMAIN=' domain here'
export ALGORITHMS=['hashing algorithm here']
export API_AUDIENCE='api audience here'
export CLIENT_ID='client ID here'
export CLIENT_SECRET_KEY='client secret key here'
```
9. **Confirm that your postgress server is running:**
```
psql database_name
```
10. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_DEBUG=true
export FLASK_ENV=development # enables debug mode
python3 app.py
```
11. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5001/) or [http://localhost:5000](http://localhost:5001)


## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

You can download and install all the dependencies needed for this project using `pip` and reading from the requirements file as:
```
pip install -r requirements.txt
```

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

## Main Files: Project Structure
Overall, this project is designed using the MVC Framework.
* Models are located in `models.py`.
* Views are located in `templates/`.
* Controllers are located in `app.py`.
* Web forms for creating data are located in `forms.py`

  ```sh
  ├── README.md
  ├── app.py # the main driver of the app. Includes your SQLAlchemy models.
  ├── app_api.py # the REST API of CAST!. Seperated from app.py to avoid a large monolith and to seperate API tests from the main application
  ├── auth
  │   ├── decorators.py # Defines "requires_auth" function, which is crucial for RBAC in this project.
  │   ├── views.py # Defines the signup, login, logout and callback functions crucial for RBAC in this project.
  ├── config.py # Database URLs, secret key setup, etc
  ├── error.log
  ├── fabfile.py
  ├── forms.py # Your forms, pulling from WTForms, a flexible forms validation and rendering library for Python web development.
  ├── manage.py # To setup Migration to initialize your database schema, and easily upgrade and downgrade
  ├── migrations
  │   ├── version # to easily upgrade and downgrade your data models using "python3 manage.py db action_here" where action can be migrate, upgrade or downgrade.
  ├── models.py # for configuration of your data models, and app, db, and migrate objects.
  ├── package.json # Functional metadata about this project
  ├── Procfile # To deploy app.py on Heroku using gunicorn
  ├── requirements.txt # The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── runtime.txt # The Python version that Heroku will use to run the deployed application
  ├── test_app_api.py # Your API unit tests, excuted with "python test_app_api.py"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

## Endpoints Documentation

Below is a detailed documentation of the API endpoints including the URL, request parameters, and the response body. Use the examples below as a reference.

### Setup To test the API in your Local Environment
1. **Run the API server:**
```
export FLASK_APP=myapp
export FLASK_DEBUG=true
export FLASK_ENV=development # enables debug mode
python3 app_api.py
```
2. **Load any of the endpoint URLs:**

Browser Example: 
```
http://127.0.0.1:5001/actors
```
Curl Example:
```
`curl http://127.0.0.1:5001/actors -X GET -H "Content-Type: application/json"`
```

## ACTORS Endpoints

### GET /actors

- Fetches a dictionary of all the actors.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/actors -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys, `actors`, `success`, and `total_actors` in the format below.

```json
{
  "actors": [
    {
      "age": 55,
      "city": "Seattle",
      "gender": "male",
      "genre": "{Adventure}",
      "id": 1,
      "image_link": "https://images.unsplash.com/photo-1676490605000-a42a43a7ccbc?q=80&w=2864&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      "instagram_link": "http://instagram.com/jamiefoxx",
      "name": "Jamie Foxx",
      "seeking_casting": "false",
      "seeking_description": "",
      "state": "NY",
      "website_link": "https://www.google.com/jamiefoxx"
    },
    {
      "age": 40,
      "city": "Nairobi",
      "gender": "female",
      "genre": "{Action,Thriller}",
      "id": 2,
      "image_link": "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?auto=format&fit=crop&q=60&w=800&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2x1YiUyMHBhcnR5fGVufDB8fDB8fHwy",
      "instagram_link": "http://instagram.com/lupita",
      "name": "Lupita Nyongo",
      "seeking_casting": "true",
      "seeking_description": "Seeking casting for the next epic Black Panther!",
      "state": "WA",
      "website_link": "http://google.com/lupita"
    }
  ],
  "success": true,
  "total_actors": 2
}
```

### GET /actors/<int:actor_id>

- Fetches an actor based on the ID provided.
- Request Arguments: `actor_id`
- Curl example: `curl http://127.0.0.1:5001/actors/2 -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys, `actor_details`, `current_actor_id`, and `success` in the format below.
```json
{
  "actor_details": {
    "age": 40,
    "city": "Nairobi",
    "gender": "female",
    "genre": "{Action,Thriller}",
    "id": 2,
    "image_link": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=2940&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=60",
    "instagram_link": "http://instagram.com/lupita",
    "name": "Lupita Nyongo",
    "past_showings": [],
    "past_showings_count": 0,
    "seeking_casting": "false",
    "seeking_description": "",
    "state": "WA",
    "upcoming_showings": [],
    "upcoming_showings_count": 0,
    "website_link": "http://google.com/lupita"
  },
  "current_actor_id": 2,
  "success": true
}
```

### GET /actors/create

- Loads the form to create a new actor.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/actors/create -X GET -H "Content-Type: application/json"`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `get_form`, and `success` in the format below: 

```json
{
  "get_form": true,
  "success": true
}
```

### POST /actors/create

- Posts the details of the new actor.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/actors/create -X POST -H "Content-Type: application/json" -d '{"name":"Mercy Test", "age":22, "gender":"female" ,"city":"Toronnno", "state":"WA", "genre":"Action", "instagram_link":"http://instagram.com/test", "website_link":"http://google.com/test", "image_link":"http://image.com/test", "seeking_casting":"true", "seeking_description":"desc test"}'`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `created_actor_name`, `success`, and `total_actors` in the format below: 

```json
{
  "created_actor_name": "Mercy Test",
  "success": true,
  "total_actors": 35
}
```

### GET /actors/<int:actor_id>/edit

- Loads a pre-filled form to edit the details selected actor.
- Request Arguments: `actor_id`
- Curl example: `curl http://127.0.0.1:5001/actors/77/edit -X GET -H "Content-Type: application/json"`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `created_actor_name`, `success`, and `total_actors` in the format below: 

```json
{
  "actor_id": 77,
  "get_form": true,
  "success": true
}
```

### POST /actors/<int:actor_id>/edit
- Updates the details of the actor selected in the database.
- Request Arguments: `actor_id`
- Curl example: `curl http://127.0.0.1:5001/actors/77/edit -X POST -H "Content-Type: application/json" -d '{"name":"Mercy Test", "age":22, "gender":"female" ,"city":"Toronnno", "state":"WA", "genre":"Action", "instagram_link":"http://instagram.com/test", "website_link":"http://google.com/test", "image_link":"http://image.com/test", "seeking_casting":"true", "seeking_description":"desc test"}'`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `actor_id`, and `success` in the format below: 

```json
{
  "actor_id": 77,
  "success": true
}
```

### GET /actors/<int:actor_id>/delete
- Deletes the specified actor from the database.
- Request Arguments: `actor_id`
- Curl example: `curl http://127.0.0.1:5001/actors/30/edit -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- **NOTE:** GET is used here because DELETE method cannot be accessed via the browser
- Returns: An object with the keys: `deleted_actor_id`, `total_actors`, and `success` in the format below: 

```json
{
  "deleted_actor_id": 30,
  "success": true,
  "total_actors": 34
}
```


## MOVIES Endpoints

### GET /movies

- Fetches a dictionary of all the movies.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/movies -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys, `movies`, `success`, and `total_movies` in the format below.

```json
{
  "movies": [
    {
      "genre": "{Action}",
      "id": 3,
      "image_link": "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?auto=format&fit=crop&q=60&w=800&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2x1YiUyMHBhcnR5fGVufDB8fDB8fHwy",
      "instagram_link": "http://instagram.com/blackpanther",
      "release_date": "2024-11-10 13:45:38",
      "seeking_actors": "false",
      "seeking_description": "",
      "title": "Black Panther",
      "website_link": "http://google.com/balckpanther"
    },
    {
      "genre": "{Drama,Other}",
      "id": 13,
      "image_link": "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?auto=format&fit=crop&q=60&w=800&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2x1YiUyMHBhcnR5fGVufDB8fDB8fHwy",
      "instagram_link": "http://instagram.com/tester",
      "release_date": "2022-11-16 13:14:11",
      "seeking_actors": "true",
      "seeking_description": "Seeking for Vanderpump Rules actors.",
      "title": "Vanderpump Rules",
      "website_link": "https://www.google2.com/test3"
    }
  ],
  "success": true,
  "total_movies": 4
}
```

### GET /movies/<int:movie_id>

- Fetches a movie based on the ID provided.
- Request Arguments: `movie_id`
- Curl example: `curl http://127.0.0.1:5001/movies/13 -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys, `movie_details`, `current_movie_id`, and `success` in the format below.
```json
{
  "current_movie_id": 13,
  "movie_details": {
    "genre": "{Drama,Other}",
    "id": 13,
    "image_link": "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?auto=format&fit=crop&q=60&w=800&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2x1YiUyMHBhcnR5fGVufDB8fDB8fHwy",
    "instagram_link": "http://instagram.com/tester",
    "past_showings": [],
    "past_showings_count": 0,
    "release_date": "2022-11-16 13:14:11",
    "seeking_actors": "true",
    "seeking_description": "Seeking for Vanderpump Rules actors.",
    "title": "Vanderpump Rules",
    "upcoming_showings": [],
    "upcoming_showings_count": 0,
    "website_link": "https://www.google2.com/test3"
  },
  "success": true
}
```

### GET /movies/create
- Loads the form to create a new movie.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/movies/create -X GET -H "Content-Type: application/json"`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `get_form`, and `success` in the format below: 

```json
{
  "get_form": true,
  "success": true
}
```

### POST /movies/create

- Posts the details of the new movie.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/movies/create -X POST -H "Content-Type: application/json" -d '{"title":"test SLY", "release_date":"2024-11-10 13:45:38", "genre":"Action", "instagram_link":"http://instagram.com/testtest", "website_link":"http://google.com/testtest", "image_link":"http://image.com/testtest", "seeking_actors":"true", "seeking_description":"seeking movies via unittest"}'`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `new_movie_name`, `success`, and `total_movies` in the format below: 

```json
{
  "new_movie_name": "test SLY",
  "success": true,
  "total_movies": 5
}
```

### GET /movies/<int:movie_id>/edit

- Loads a pre-filled form to edit the details selected movie.
- Request Arguments: `movie_id`
- Curl example: `curl http://127.0.0.1:5001/movies/16/edit -X GET -H "Content-Type: application/json"`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `created_actor_name`, `success`, and `total_actors` in the format below: 

```json
{
  "get_form": true,
  "movie_id": 16,
  "success": true
}
```

### POST /movies/<int:movie_id>/edit
- Updates the details of the movie selected in the database.
- Request Arguments: `movie_id`
- Curl example: `curl http://127.0.0.1:5001/movies/16/edit -X POST -H "Content-Type: application/json" -d '{"title":"SLY docuseries", "release_date":"2024-12-10 13:45:38", "genre":"Action", "instagram_link":"http://instagram.com/sly", "website_link":"http://google.com/sly", "image_link":"http://image.com/testtest", "seeking_actors":"true", "seeking_description":"seeking actors for the 2nd season"}'`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `movie_id`, and `success` in the format below: 

```json
{
  "movie_id": 16,
  "success": true
}
```

### GET /movies/<int:movie_id>/delete
- Deletes the specified movie from the database.
- Request Arguments: `movie_id`
- Curl example: `curl http://127.0.0.1:5001/movies/15/delete -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- **NOTE:** GET is used here because DELETE method cannot be accessed via the browser
- Returns: An object with the keys: `deleted_movie_id`, `total_movies`, and `success` in the format below: 

```json
{
  "deleted_movie_id": 15,
  "success": true,
  "total_movies": 6
}
```


## SHOWINGS Endpoints
### GET /showings

- Fetches a dictionary of all the showings.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/showings -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys, `all_showings`, `success`, and `total_showings` in the format below.

```json
{
  "all_showings": [
    {
      "actor_id": 1,
      "actor_name": "Sylvester Stallone",
      "id": 2,
      "movie_id": 4,
      "movie_image_link": "http://unsplash.com/image",
      "movie_title": "SLY",
      "start_time": "2023-11-11 15:02:42"
    },
    {
      "actor_id": 3,
      "actor_name": "Lupita Nyongo",
      "id": 4,
      "movie_id": 3,
      "movie_image_link": "http://unsplash.com/image",
      "movie_title": "Black Panther",
      "start_time": "2023-11-11 16:07:50"
    }
  ],
  "success": true,
  "total_showings": 2
}
```


### GET /showings/create
- Loads the form to create a new showing.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/showings/create -X GET -H "Content-Type: application/json"`
- Failed query will return a 404 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `get_form`, and `success` in the format below: 

```json
{
  "get_form": true,
  "success": true
}
```

### POST /showings/create

- Posts the details of the new showing.
- Request Arguments: None
- Curl example: `curl http://127.0.0.1:5001/showings/create -X POST -H "Content-Type: application/json" -d '{"actor_id":3, "movie_id":4, "start_time":"2024-11-10 13:45:38"}'`
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- Returns: An object with the keys: `showing_lead_actor_id`, `success`, and `total_showings` in the format below: 

```json
{
  "showing_lead_actor_id": 3,
  "success": true,
  "total_showings": 7
}
```


## Hosting on Heroku (Deplyment via CLI and Git)
- Signup on [Heroku](https://signup.heroku.com/)
- Install the Heroku CLI by running the command below (you'll be prompted to login too):
```
curl https://cli-assets.heroku.com/install.sh | sh
```
- Build your application locally.
>**Note** - This includes generating your migration files which we use in this project to create our Data models in the postgres database. Use the commands below to run your migrations;
```
python3 manage.py db init #to initialize your migrations file
python3 manage.py db migrate #to create a new migration file
python3 manage.py db upgrade #to apply the migration created; upgrade can be changed to downgrade to rollback the migration
```
- Create a file, ```Procfile```, in your root directory, and add the command below:
```
web: gunicorn app:app
```
- Create a file, ```runtime.txt```, in your root directory, and add the Python version Heroku will use to run your deployed application, example below:
```
python-3.9.18
```
- Add heroku as a remote
```
git init #initialize a git repo for your project
git remote add heroku #add heroku as a remote
git branch -M main
git add . #to add all the files you want to track on Heroku
git commit -m "initial commit"
```
- [Create a Heroku application](https://devcenter.heroku.com/articles/creating-apps) with the folling command on CLI:
```
heroku create my-amazing-application
```
- Add [Heroku Postgres](https://www.heroku.com/postgres) as a resource under your heroku application via your Heroku dashboard or via CLI with the command below. This will add a postgres database on heroku that can be used by your application.
```
heroku addons:create heroku-postgresql:PLAN_NAME
```
- Push the Git repository you've created using the command below to trigger the build and deploy process:
```
git push heroku main
```
- Run the latest database migration on heroku CLI to create the latest database model on your app on Heroku. (_my-amazing-application_ is the name of my app on Heroku)
```
heroku run python manage.py db upgrade --app my-amazing-application
```
- Test your Heroku-hosted application online. You can either run the command below on CLI, or check heroku logs or your Heroku dashboard for the URL.
```
heroku open
```

### Continuous Deployment via GitHub
- To make it easy to deply code on GitHub to your app on Heroku, you can setup Heroku GitHub deployments by following the [steps on this tutorial.](https://devcenter.heroku.com/articles/github-integration)


### Creating a new Heroku Postgres Database mid-project
Follow the instructions below if you are setting up  your database and data models afresh mid-project i.e. after the initial setup.

- Delete the ```Migrations``` directory on your local repository.
- Delete and then create the database locally with the commands below:
```
dropdb NAME_OF_OLD_DB
createdb NAME_OF_NEW_DB
```
- Create a new migration and upgrade using the commands below:
```
python3 manage.py db init # to initialize the migrations directory
python3 manage.py db migrate # details the model changes to be made with upgrade and downgrade logic setup
python3 manage.py db upgrade # to apply the migration
```
- Push your project changes to GitHub, then deploy to Heroku.
- Delete the existing database on Heroku via Heroku Dashboard --> Resources.
- Add a new Heroku Postgres database under _Resources_ on your Heroku dashboard.
- Run the latest migration upgrade on your Heroku database via CLI with the command below:
```
heroku run python manage.py db upgrade --app YOUR_HEROKU_APP_NAME
```
- To check the changes on your Heroku database via CLI, run:
```
heroku psql
```


## Authentication with Auth0
-


## Authorization with Auth0
-


## Appreciation
My hearfelt appreciation to:
1. Udacity; for an amazing Web Developemnt Nanodegree program that gave me a platform to refresh my software engineering skills, and for providing the boiler-plate for this code-base.
2. My friends Ade, Warugz, and Soni; for the motivation to push through :)

