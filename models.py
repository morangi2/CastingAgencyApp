#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

app = Flask(__name__) #in app.py = OK
moment = Moment(app) # NOWHERE, for formatting dates and times
app.config.from_object('config') #in models.py = OK
db = SQLAlchemy(app) #in models.py = OK
migrate = Migrate(app, db) #in manage.py + manager == OK

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


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate == DONE
    #     -- Done; added a migrate object above to enable use of Flask-Migrate

    genres = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f'<NEW VENUE: {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.genres} {self.website_link} {self.seeking_talent} {self.seeking_description}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate == DONE
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
       return f'<NEW ARTIST: {self.id} {self.name} {self.city} {self.state} {self.phone} {self.image_link} {self.facebook_link} {self.genres} {self.website_link} {self.seeking_venue} {self.seeking_description}>'


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. == DONE

class Show(db.Model):
   __tablename__ = 'shows'

   id = db.Column(db.Integer, primary_key=True)
   artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
   venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
   start_time = db.Column(db.String(120), nullable=False)

   def __repr__(self):
      return f'<NEW SHOW: {self.id} {self.start_time}, list {self.artist_id} {self.venue_id}>'
