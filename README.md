## CAST! The Casting Agency App
CAST! is the name of this Casting Agency Application. The Executive Producer at CAST! had a major painpoint; that it was very difficult to trace which movie is assigned to which starring actor (and vice versa) and which showings have been confirmed alongside their respective details. As the lead software engineer, my main motivation for creating CAST! was to create a system to simplify and streamline the process of showcasing and accessing the details of movies, starring actors, and showings.

### How to access CAST!
- Public URL: https://castingagency-mjko-c1b260bbded2.herokuapp.com/
- **NOTE:** Accessing CAST! beyond the home-page requires authentication. Feel free to sign-up on the screen that shows up, and relevant roles will be granted within 24 hours.

### V1 of CAST! 
This is what you currently see in this app, which incoporates 3 major functionalities;
1. Movies; posting a new movie, viewing a list of movies, viewing the details of a specific movie (including past and upcoming showings and if they are seeking casting opportunities), editing and deleting a specific movie.
2. Actors; posting a new starring actor, viewing a list of starring actors grouped by geographical location, viewing the details of a specific actor (including past and upcoming showings and if they are seeking casting opportunities), editing and deleting a starring actor.
3. Showings; posting a new showwing which highlights the movie that will be showed, alongside the starring actor, and the date and time of the showing.

### V2 of CAST!
This will be the 2nd iteration of the app adding onto the functionality above as illustrated below;
1. Movies; add the details of the producers of the movie
2. Actors; include other actors (not just starring actors) and tag them accordingly
3. Showings; include the details of the cinemas (and locations) where the showing will take place, and tag more actors in a given showing.

### Appreciation
My hearfelt appreciation to:
1. Udacity; for an amazing Web Developemnt Nanodegree program that gave me a platform to refresh my software engineering skills, and for providing the boiler-plate for this code-base.
2. My friends q_ode and Mo; for the motivation to push through :)


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

- Loads the form to create a new actor.
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
- Loads a pre-filled form to edit the details selected actor.
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
- Failed query will return a 400 error. See Errors section below for more details of the `key:value` pairs returned.
- **NOTE:** GET is used here because DELETE method cannot be accessed via the browser
- Returns: An object with the keys: `deleted_actor_id`, `total_actors`, and `success` in the format below: 

```json
{
  "deleted_actor_id": 30,
  "success": true,
  "total_actors": 34
}
```
