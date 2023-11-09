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
