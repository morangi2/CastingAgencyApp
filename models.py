#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from auth.views import auth_bp

app = Flask(__name__) #in app.py = OK
moment = Moment(app) # NOWHERE, for formatting dates and times
app.config.from_object('config') #in models.py = OK
db = SQLAlchemy(app) #in models.py = OK
migrate = Migrate(app, db) #in manage.py + manager == OK
app.register_blueprint(auth_bp, url_prefix='/')


class Actor(db.Model):
   __tablename__ = 'actors'
   
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String, nullable=False)
   age = db.Column(db.Integer, nullable=False)
   gender = db.Column(db.String, nullable=False)
   city = db.Column(db.String, nullable=False)
   state = db.Column(db.String, nullable=False)
   genre = db.Column(db.String, nullable=False)
   instagram_link = db.Column(db.String, nullable=False)
   website_link = db.Column(db.String, nullable=False)
   image_link = db.Column(db.String, nullable=False)
   seeking_casting = db.Column(db.String, nullable=False)
   seeking_description = db.Column(db.String, nullable=False)
   show = db.relationship('Showing', backref='actor', lazy=True)

   def __repr__(self):
      return f'<NEW ACTOR: {self.id} {self.name} {self.age} {self.gender} {self.city} {self.state} {self.genre} {self.instagram_link} {self.website_link} {self.image_link} {self.seeking_casting} {self.seeking_description}>'
  
class Movie(db.Model):
   __tablename__ = 'movies'

   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String, nullable=False)
   release_date = db.Column(db.String, nullable=False)
   genre = db.Column(db.String, nullable=False)
   instagram_link = db.Column(db.String, nullable=False)
   website_link = db.Column(db.String, nullable=False)
   image_link = db.Column(db.String, nullable=False)
   seeking_actors = db.Column(db.String, nullable=False)
   seeking_description = db.Column(db.String, nullable=False)
   showing = db.relationship('Showing', backref='movie', lazy=True)

   def __repr__(self):
      return f'<NEW MOVIE: {self.id} {self.title} {self.release_date} {self.genre} {self.instagram_link} {self.website_link} {self.image_link} {self.seeking_actors} {self.seeking_description}>'
   
class Showing(db.Model):
   __tablename__ = 'showings'

   id = db.Column(db.Integer, primary_key=True)
   actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
   #actor_id_2 = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=True)
   movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
   start_time = db.Column(db.String, nullable=False)

   def __repr__(self):
      return f'<NEW SHOWING: {self.id} {self.actor_id} {self.movie_id} {self.start_time}>'

