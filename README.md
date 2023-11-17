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
