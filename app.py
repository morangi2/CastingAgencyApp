#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
import dateutil.parser
import babel
from flask import abort, render_template, request, flash, redirect, url_for
#from markupsafe import Markup
import logging
from logging import Formatter, FileHandler
from sqlalchemy import and_, or_ 
from forms import *
import sys, time
from models import *
import re
from wtforms import ValidationError
import os
#----------------------------------------------------------------------------#
# App Config.
# TODO: Refactored to file models.py == DONE
#----------------------------------------------------------------------------#
# TODO: connect to a local postgresql database == DONE
#----------------------------------------------------------------------------#
# Models.
# TODO: Refactored to file models.py == DONE
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  excited = os.environ['EXCITED']
  if excited == 'true':
    print("***EXCITED is true!!********")
    print(os.environ['DATABASE_URL'])
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  ACTORS
#   -get all, get by ID, post new, patch by ID, delete one
#  ----------------------------------------------------------------

@app.route('/actors')
def actors():
  actors_list = Actor.query.distinct('city')
  actors = []

  for one_actor in actors_list:
    actor_data = {}
    """ actor_data['name'] = one_actor.name
    actor_data['age'] = one_actor.age
    actor_data['gender'] = one_actor.gender """
    actor_data['city'] = one_actor.city
    actor_data['state'] = one_actor.state
    actor_data['actors'] = Actor.query.filter_by(city = one_actor.city)
    actor_data['num_upcoming_showings'] = Showing.query.filter_by(actor_id = one_actor.id).count()
    actors.append(actor_data)

  return render_template('pages/actors.html', actors=actors)

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
  actor_form = ActorForm()
  return render_template('forms/new_actor.html', form=actor_form)

@app.route('/actors/create', methods=['POST'])
def create_actor_submission():
  error = False
  actor_name = ''
  data = {}

  try:
    form = ActorForm(request.form)

    actor = Actor(name = form.name.data,
                  age = form.age.data,
                  gender = form.gender.data,
                  city = form.city.data,
                  state = form.state.data,
                  genre = form.genre.data,
                  instagram_link = form.instagram_link.data,
                  website_link = form.website_link.data,
                  image_link = form.image_link.data,
                  seeking_casting = form.seeking_casting.data,
                  seeking_description = form.seeking_description.data)
    
    db.session.add(actor)
    db.session.commit()

    actor_name = form.name.data

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
  
  if error:
    error = False
    print(sys.exc_info())
    flash('An ERROR occured. Actor ' + actor_name + ' could not be added.')
  else:
    flash('Actor ' + actor_name + ' added successfully!')

  return render_template('pages/home.html')


@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):
  error = False

  try:
    actor_selected_data = {}
    actor_selected = Actor.query.get(actor_id)
    showings_joinedwith_movies = Showing.query.filter_by(actor_id=actor_id).join(Movie).all()

    actor_selected_data['id'] = actor_selected.id
    actor_selected_data['name'] = actor_selected.name
    actor_selected_data['age'] = actor_selected.age
    actor_selected_data['gender'] = actor_selected.gender
    actor_selected_data['city'] = actor_selected.city
    actor_selected_data['state'] = actor_selected.state
    actor_selected_data['genre'] = actor_selected.genre
    actor_selected_data['instagram_link'] = actor_selected.instagram_link
    actor_selected_data['website_link'] = actor_selected.website_link
    actor_selected_data['image_link'] = actor_selected.image_link
    actor_selected_data['seeking_casting'] = actor_selected.seeking_casting
    actor_selected_data['seeking_description'] = actor_selected.seeking_description
    actor_selected_data['upcoming_showings_count'] = 0
    actor_selected_data['upcoming_showings'] = []
    actor_selected_data['past_showings_count'] = 0
    actor_selected_data['past_showings'] = []

    for showing in showings_joinedwith_movies:
      this_showing = {}
      this_showing['actor_id'] = showing.actor_id
      this_showing['actor_image_link'] = showing.actor.image_link
      this_showing['actor_name'] = showing.actor.name
      this_showing['start_time'] = showing.start_time

      showing_start_time = showing.start_time
      showing_start_time_formatted = datetime.strptime(showing_start_time, '%Y-%m-%d %H:%M:%S')
      timestamp_db = datetime.timestamp(showing_start_time_formatted)
      timestamp_current = time.time()

      if timestamp_current > timestamp_db:
        actor_selected_data['past_showings_count'] += 1
        actor_selected_data['past_showings'].append(this_showing)
      else:
        actor_selected_data['upcoming_showings_count'] += 1
        actor_selected_data['upcoming_showings'].append(this_showing)

  except:
    error = True
    print(sys.exc_info())
  if error:
    error = False
    flash('This actor does NOT exist in our records.')
    return render_template('pages/home.html')
  
  return render_template('pages/show_actor.html', actor=actor_selected_data)


@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
  form = ActorForm()
  actor_data = {}
  actor_to_edit = Actor.query.get(actor_id)

  #pass all the actor data
  actor_data['id'] = actor_to_edit.id
  actor_data['name'] = actor_to_edit.name
  actor_data['age'] = actor_to_edit.age
  actor_data['gender'] = actor_to_edit.gender
  actor_data['genre'] = actor_to_edit.genre
  actor_data['city'] = actor_to_edit.city
  actor_data['state'] = actor_to_edit.state
  actor_data['image_link'] = actor_to_edit.image_link
  actor_data['website_link'] = actor_to_edit.website_link
  actor_data['instagram_link'] = actor_to_edit.instagram_link
  actor_data['seeking_casting'] = actor_to_edit.seeking_casting
  actor_data['seeking_description'] = actor_to_edit.seeking_description

  print('****CASTING SEEKING EDIT/GET******')
  print(actor_to_edit.seeking_casting)

  #populate the form with existing actor data
  form.name.data = actor_to_edit.name
  form.age.data = actor_to_edit.age
  form.gender.data = actor_to_edit.gender
  form.genre.data = actor_to_edit.genre
  form.city.data = actor_to_edit.city
  form.state.data = actor_to_edit.state
  form.image_link.data = actor_to_edit.image_link
  form.instagram_link.data = actor_to_edit.instagram_link
  form.website_link.data = actor_to_edit.website_link
  form.seeking_casting.data = actor_to_edit.seeking_casting
  form.seeking_description.data = actor_to_edit.seeking_description

  print('****CASTING SEEKING EDIT/POST/form display******')
  print(form.seeking_casting.data)

  return render_template('/forms/edit_actor.html', form = form, actor = actor_data)

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):
  error = False

  try:
    #actor to edit
    actor_edit = Actor.query.get(actor_id)
    #form details
    form = ActorForm(request.form)

    actor_edit.name = form.name.data
    actor_edit.age = form.age.data
    actor_edit.gender = form.gender.data
    actor_edit.genre = form.genre.data
    actor_edit.city = form.city.data
    actor_edit.state = form.state.data
    actor_edit.instagram_link = form.instagram_link.data
    actor_edit.website_link = form.website_link.data
    actor_edit.image_link = form.image_link.data
    actor_edit.seeking_casting = form.seeking_casting.data
    actor_edit.seeking_description = form.seeking_description.data

    print('****CASTING SEEKING EDIT/POST******')
    print(form.seeking_casting.data)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    flash('Edit was UNSUCCESSFUL! Please try again.')
    abort(404)
  else:
    flash('Edit was successful!')

  return redirect(url_for('show_actor', actor_id = actor_id))


@app.route('/actors/<int:actor_id>/delete', methods=['GET'])
def delete_actor(actor_id):
  error = False

  try:
    Actor.query.filter_by(id = actor_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    flash('Actor successfully deleted!')
  if error:
    error = False
    flash('An error occured. Venue not deleted.')
    abort(404)

  return redirect(url_for('index'))


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive. == DONE
  # seach for Hop should return "The Musical Hop". == DONE
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" == DONE
  # TODO: BONUS Challenge: == DONE
  #       Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.

  search_term = request.form['search_term']
  search_term_incomplete = '%' + search_term + '%'

  #search by city AND state if someone enters both, comma separated eg searching for "Toronto, ON" will give you venues specifically under Toronto, ON
  search_term_city = ''
  search_term_state = ''
  search_term_split = search_term.split(', ')
  length_of_split = len(search_term_split)

  if length_of_split == 2:
    #seperate by the comma
    search_term_city = search_term_split[0]
    search_term_state = search_term_split[1]
  else:
    search_term_city = search_term
    search_term_state = search_term

  search_response = {}
  search_response['count'] = 0
  search_response['data'] = []

  #venues_from_search = Venue.query.filter(Venue.name.contains(search_term)) ## ==> .contains() is not case-insensitive
  #venues_from_search = Venue.query.filter(Venue.name.ilike(search_term_incomplete)) ## ==> searches only for the venue name
  # below: search by incomplete name, or specific city, or specific state
  venues_from_search = Venue.query.filter(or_(Venue.name.ilike(search_term_incomplete), and_(Venue.state.contains(search_term_state), Venue.city.contains(search_term_city))))
  venues_from_search_count = Venue.query.filter(or_(Venue.name.ilike(search_term_incomplete), and_(Venue.state.contains(search_term_state), Venue.city.contains(search_term_city)))).count()

  for venue in venues_from_search:
    this_venue = {}
    this_venue['id'] = venue.id
    this_venue['name'] = venue.name
    this_venue['num_upcoming_shows'] = Show.query.filter_by(venue_id = venue.id).count()

    search_response['count'] = venues_from_search_count
    search_response['data'].append(this_venue)

  return render_template('pages/search_venues.html', results=search_response, search_term=search_term)


#  ----------------------------------------------------------------
#  MOVIES
#  ----------------------------------------------------------------

@app.route('/movies')
def movies():
  all_movies = Movie.query.all()
  movie_data = []

  for movie in all_movies:
    movie_formatted = {}
    movie_formatted['id'] = movie.id
    movie_formatted['title'] = movie.title
    movie_data.append(movie_formatted)

  return render_template('pages/movies.html', movies = movie_data)


#2 methods for /movies/create route: get the form, then post the entry
@app.route('/movies/create', methods=['GET'])
def create_movie_form():
  form = MovieForm()

  return render_template('forms/new_movie.html', form = form)

@app.route('/movies/create', methods=['POST'])
def create_movie_submission():
  error = False
  movie_title = ''

  try:
    form = MovieForm(request.form)
    movie = Movie(title = form.title.data,
                  release_date = form.release_date.data,
                  genre = form.genre.data,
                  website_link = form.website_link.data,
                  image_link = form.image_link.data,
                  instagram_link = form.instagram_link.data,
                  seeking_actors = form.seeking_actors.data,
                  seeking_description = form.seeking_description.data)
    
    movie_title = form.title.data
    db.session.add(movie)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('ERROR: Movie was not added to our records.')
  finally:
    db.session.close()
  if error:
    error = False
    print(sys.exc_info())
  else:
    flash('Movie ' + movie_title + ' was successfully listed!')
  
  return render_template('pages/home.html')


@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
  error = False

  try:
    movie_selected = Movie.query.get(movie_id)
    showings_joinedwith_actors = Showing.query.filter_by(movie_id = movie_id).join(Actor).all()

    movie_selected_data = {}

    movie_selected_data['id'] = movie_selected.id
    movie_selected_data['title'] = movie_selected.title
    movie_selected_data['release_date'] = movie_selected.release_date
    movie_selected_data['genre'] = movie_selected.genre
    movie_selected_data['website_link'] = movie_selected.website_link
    movie_selected_data['instagram_link'] = movie_selected.instagram_link
    movie_selected_data['image_link'] = movie_selected.image_link
    movie_selected_data['seeking_actors'] = movie_selected.seeking_actors
    movie_selected_data['seeking_description'] = movie_selected.seeking_description
    movie_selected_data['past_showings'] = []
    movie_selected_data['upcoming_showings'] = []
    movie_selected_data['past_showings_count'] = 0
    movie_selected_data['upcoming_showings_count'] = 0

    for showing in showings_joinedwith_actors:
      this_showing = {}
      this_showing['actor_id'] = showing.actor_id
      this_showing['actor_name'] = showing.actor.name
      this_showing['actor_image_link'] = showing.actor.image_link
      this_showing['start_time'] = showing.start_time

      showing_start_time = showing.start_time
      showing_start_time_formatted = datetime.strptime(showing_start_time, '%Y-%m-%d %H:%M:%S')
      timestamp_db = datetime.timestamp(showing_start_time_formatted)
      timestamp_current = time.time()

      if timestamp_current > timestamp_db:
        movie_selected_data['past_showings'].append(this_showing)
        movie_selected_data['past_showings_count'] += 1
      else:
        movie_selected_data['upcoming_showings'].append(this_showing)
        movie_selected_data['upcoming_showings_count'] += 1

  except:
    error = True
    print(sys.exc_info())
  if error:
    error = False
    flash('This Movie does NOT exist in our records.')
    abort(404)
  
  return render_template('pages/show_movie.html', movie = movie_selected_data)


# patch movie
# uses 2 methods; edit/get to load preexisting data, and edit/post to post changes made
@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):
  form = MovieForm()
  movie_to_edit = Movie.query.get(movie_id)
  print('*******MOVIE TO EDIT *******')
  
  movie_data = {}

  #load movie object
  movie_data['id'] = movie_to_edit.id
  movie_data['title'] = movie_to_edit.title
  movie_data['release_date'] = movie_to_edit.release_date
  movie_data['genre'] = movie_to_edit.genre
  movie_data['website_link'] = movie_to_edit.website_link
  movie_data['instagram_link'] = movie_to_edit.instagram_link
  movie_data['image_link'] = movie_to_edit.image_link
  movie_data['seeking_actors'] = movie_to_edit.seeking_actors
  movie_data['seeking_description'] = movie_to_edit.seeking_description


  #load form object
  form.title.data = movie_to_edit.title
  #form.release_date.data = movie_to_edit.release_date
  form.genre.data = movie_to_edit.genre
  form.website_link.data = movie_to_edit.website_link
  form.image_link.data = movie_to_edit.image_link
  form.instagram_link.data = movie_to_edit.instagram_link
  form.seeking_actors.data = movie_to_edit.seeking_actors
  form.seeking_description.data = movie_to_edit.seeking_description

  print('*******RELEASE DATE*******')
  print(type(form.release_date.data))
 

  return render_template('forms/edit_movie.html', form=form, movie=movie_data)



@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):
  error = False
  form = MovieForm(request.form)

  try:
    movie_to_edit = Movie.query.get(movie_id)

    movie_to_edit.title = form.title.data
    movie_to_edit.release_date = form.release_date.data
    movie_to_edit.genre = form.genre.data
    movie_to_edit.website_link = form.website_link.data
    movie_to_edit.image_link = form.image_link.data
    movie_to_edit.instagram_link = form.instagram_link.data
    movie_to_edit.seeking_actors = form.seeking_actors.data
    movie_to_edit.seeking_description = form.seeking_description.data

    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    flash('an error occured, edit unsuccessful.')
    abort(500)
  else:
    flash('edit was successfull!')

  return redirect(url_for('show_movie', movie_id = movie_id))



@app.route('/movies/<int:movie_id>/delete', methods = ['GET'])
def delete_movie(movie_id):
  error = False
  try:
    Movie.query.filter_by(id = movie_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    flash('An error occured. Deletion not successful.')
    abort(404)
  else:
    flash('Movie successfully deleted.')

  return render_template('pages/home.html')





#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database == DONE

  artist_data = []
  artists_all = Artist.query.all()

  for artist in artists_all:
    artist_formatted = {}
    artist_formatted['id'] = artist.id
    artist_formatted['name'] = artist.name
    artist_data.append(artist_formatted)

  return render_template('pages/artists.html', artists=artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. == DONE
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band". == DONE
  # search for "band" should return "The Wild Sax Band". == DONE
  # TODO: BONUS Challenge: == DONE
  #       Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.

  search_term = request.form['search_term']
  search_term_case_insensitive = '%' + search_term + '%'

  #search by CITY and STATE if someone enters both, comma seperated. EG: searching for "Seattle, WA" will give you artists specifically under Seattle, WA
  search_term_city = ''
  search_term_state = ''
  search_term_split = search_term.split(', ')
  length_of_split = len(search_term_split)

  if length_of_split == 2:
    #seperate by the comma
    search_term_city = search_term_split[0]
    search_term_state = search_term_split[1]
  else:
    search_term_city = search_term
    search_term_state = search_term

  search_response = {}
  search_response['count'] = 0
  search_response['data'] = []

  # artists_from_search = Artist.query.filter(Artist.name.ilike(search_term_case_insensitive)) ## ==> searches only for the artist name
  artists_from_search = Artist.query.filter(or_(Artist.name.ilike(search_term_case_insensitive), and_(Artist.state.contains(search_term_state), Artist.city.contains(search_term_city))))
  artists_from_search_count = Artist.query.filter(or_(Artist.name.ilike(search_term_case_insensitive), and_(Artist.state.contains(search_term_state), Artist.city.contains(search_term_city)))).count()

  for artist in artists_from_search:
    this_artist = {}
    this_artist['id'] = artist.id
    this_artist['name'] = artist.name
    this_artist['num_upcoming_shows'] = Show.query.filter_by(artist_id = artist.id).count()

    search_response['count'] = artists_from_search_count
    search_response['data'].append(this_artist)

  return render_template('pages/search_artists.html', results=search_response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id == DONE

  error = False
  try:
    artist_selected = Artist.query.get(artist_id)
    shows_joinedwith_venue = Show.query.filter_by(artist_id = artist_id).join(Venue).all()
    artist_selected_data = {}

    artist_selected_data['id'] = artist_selected.id
    artist_selected_data['name'] = artist_selected.name
    artist_selected_data['genres'] = artist_selected.genres
    artist_selected_data['city'] = artist_selected.city
    artist_selected_data['state'] = artist_selected.state
    artist_selected_data['phone'] = artist_selected.phone
    artist_selected_data['seeking_venue'] = artist_selected.seeking_venue
    artist_selected_data['image_link'] = artist_selected.image_link
    artist_selected_data['facebook_link'] = artist_selected.facebook_link
    artist_selected_data['website'] = artist_selected.website_link
    artist_selected_data['seeking_description'] = artist_selected.seeking_description
    artist_selected_data['past_shows'] = []
    artist_selected_data['upcoming_shows'] = []
    artist_selected_data['past_shows_count'] = 0
    artist_selected_data['upcoming_shows_count'] = 0

    for show in shows_joinedwith_venue:
      this_show = {}
      this_show['venue_id'] = show.venue_id
      this_show['venue_name'] = show.venue.name
      this_show['venue_image_link'] = show.venue.image_link
      this_show['start_time'] = show.start_time

      showstart_time = show.start_time
      showstart_time_formatted = datetime.strptime(showstart_time, '%Y-%m-%d %H:%M:%S')
      db_timestamp = datetime.timestamp(showstart_time_formatted)
      current_timestamp = time.time()

      if (current_timestamp > db_timestamp):
        artist_selected_data['past_shows'].append(this_show)
        artist_selected_data['past_shows_count'] += 1
      else:
        artist_selected_data['upcoming_shows'].append(this_show)
        artist_selected_data['upcoming_shows_count'] += 1
  except:
    error = True
    print(sys.exc_info())
  if error:
    error = False
    flash('This artist does NOT exist in our records.')
    abort(404)

  return render_template('pages/show_artist.html', artist=artist_selected_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
 
  # TODO: populate form with fields from artist with ID <artist_id> == DONE

  artist_to_edit = Artist.query.get(artist_id)

  artist_data = {}
  artist_data['id'] = artist_to_edit.id
  artist_data['name'] = artist_to_edit.name
  artist_data['genres'] = artist_to_edit.genres
  artist_data['city'] = artist_to_edit.city
  artist_data['state'] = artist_to_edit.state
  artist_data['phone'] = artist_to_edit.phone
  artist_data['website_link'] = artist_to_edit.website_link
  artist_data['facebook_link'] = artist_to_edit.facebook_link
  artist_data['seeking_venue'] = artist_to_edit.seeking_venue
  artist_data['seeking_description'] = artist_to_edit.seeking_description
  artist_data['image_link'] = artist_to_edit.image_link

  form.name.data = artist_to_edit.name
  form.genres.data = artist_to_edit.genres
  form.city.data = artist_to_edit.city
  form.state.data = artist_to_edit.state
  form.phone.data = artist_to_edit.phone
  form.website_link.data = artist_to_edit.website_link
  form.facebook_link.data = artist_to_edit.facebook_link
  form.seeking_venue.data = artist_to_edit.seeking_venue
  form.seeking_description.data = artist_to_edit.seeking_description
  form.image_link.data = artist_to_edit.image_link

  return render_template('forms/edit_artist.html', form=form, artist=artist_data)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing artist record with ID <artist_id> using the new attributes == DONE

  error = False

  try:
    artist_edit = Artist.query.get(artist_id)
    form = ArtistForm(request.form)

    artist_edit.name = form.name.data
    artist_edit.genres = form.genres.data
    artist_edit.city = form.city.data
    artist_edit.state = form.state.data
    artist_edit.phone = form.phone.data
    artist_edit.website_link = form.website_link.data
    artist_edit.facebook_link = form.facebook_link.data
    artist_edit.seeking_venue = form.seeking_venue.data
    artist_edit.seeking_description = form.seeking_description.data
    artist_edit.image_link = form.image_link.data

    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    flash('Error occured: edit was not successfull.')
    abort(404)
  else:
    flash('Artist ' + request.form['name'] + ' updated successully.')

  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id> == DONE

  venue_to_edit = Venue.query.get(venue_id)

  venue_data = {}
  venue_data['id'] = venue_to_edit.id
  venue_data['name'] = venue_to_edit.name
  venue_data['genres'] = venue_to_edit.genres
  venue_data['address'] = venue_to_edit.address
  venue_data['city'] = venue_to_edit.city
  venue_data['state'] = venue_to_edit.state
  venue_data['phone'] = venue_to_edit.phone
  venue_data['website_link'] = venue_to_edit.website_link
  venue_data['facebook_link'] = venue_to_edit.facebook_link
  venue_data['seeking_talent'] = venue_to_edit.seeking_talent
  venue_data['seeking_description'] = venue_to_edit.seeking_description
  venue_data['image_link'] = venue_to_edit.image_link

  form.name.data = venue_to_edit.name
  form.genres.data = venue_to_edit.genres
  form.address.data = venue_to_edit.address
  form.city.data = venue_to_edit.city
  form.state.data = venue_to_edit.state
  form.phone.data = venue_to_edit.phone
  form.website_link.data = venue_to_edit.website_link
  form.facebook_link.data = venue_to_edit.facebook_link
  form.seeking_talent.data = venue_to_edit.seeking_talent
  form.seeking_description.data = venue_to_edit.seeking_description
  form.image_link.data = venue_to_edit.image_link

  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing venue record with ID <venue_id> using the new attributes == DONE

  error = False

  try:
    venue_edit = Venue.query.get(venue_id)
    form = VenueForm(request.form)

    venue_edit.name = form.name.data
    venue_edit.genres = form.genres.data
    venue_edit.address = form.address.data
    venue_edit.city = form.city.data
    venue_edit.state = form.state.data
    venue_edit.phone = form.phone.data
    venue_edit.website_link = form.website_link.data
    venue_edit.facebook_link = form.facebook_link.data
    venue_edit.seeking_talent = form.seeking_talent.data
    venue_edit.seeking_description = form.seeking_description.data
    venue_edit.image_link = form.image_link.data

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    flash('Venue NOT updated: something went wrong!')
    abort(404)
  else:
    flash('Venue ' + request.form['name'] + ' updated successfully!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead == DONE
  # TODO: modify data to be the data object returned from db insertion == DONE

  error = False
  artist_name = ''
  artist_data = {}

  try:
    #leverage the WTForm wrappers
    form = ArtistForm(request.form)

    artist = Artist(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  image_link = form.image_link.data,
                  facebook_link = form.facebook_link.data,
                  website_link = form.website_link.data,
                  seeking_venue = form.seeking_venue.data,
                  seeking_description = form.seeking_description.data)
    
    db.session.add(artist)
    db.session.commit()

    artist_name = form.name.data

    artist_data['id'] = artist.id
    artist_data['id'] = artist.id
    artist_data['name'] = artist.name
    artist_data['city'] = artist.city
    artist_data['state'] = artist.state
    artist_data['phone'] = artist.phone
    artist_data['genres'] = artist.genres
    artist_data['image_link'] = artist.image_link
    artist_data['facebook_link'] = artist.facebook_link
    artist_data['website_link'] = artist.website_link
    artist_data['seeking_venue'] = artist.seeking_venue
    artist_data['seeking_description'] = artist.seeking_description

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead. == DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occured. Artist ' + artist_name + ' could NOT be listed.')
  else:
    # on successful db insert, flash success
    flash('Artist ' + artist_name + ' was successfully listed!')
  
  return render_template('pages/home.html', artists=artist_data)
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. == DONE
  print("********INSIDE SHOWS**********")
  all_shows = Show.query.all()
  shows_data = []

  #traverse all shows and get the required show, venue and artist data for our view
  for show in all_shows:
    this_show = {}
    this_show['venue_id'] = show.venue_id
    this_show['venue_name'] = show.venue.name
    this_show['artist_id'] = show.artist_id
    this_show['artist_name'] = show.artist.name
    this_show['artist_image_link'] = show.artist.image_link
    this_show['start_time'] = show.start_time

    shows_data.append(this_show)

  return render_template('pages/shows.html', shows=shows_data)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead == DONE

  error = False
  error_date_format = False

  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    date_format = '%Y-%m-%d %H:%M:%S'

    #try validating the date, raise ValueError otherwise
    dateObject = datetime.strptime(start_time, date_format)
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)

    db.session.add(show)
    db.session.commit()
  except ValueError:
    error_date_format = True
    db.session.rollback()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error or error_date_format:
    # TODO: on unsuccessful db insert, flash an error instead. == DONE
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    if error:
      error = False
      flash('An error occured, show not be listed: Incorrect artist ID or venue ID')
    else:
      error_date_format = False
      flash('An error occured, show not listed: Incorrect date format, should be YYYY-MM-DD HR:MIN:SEC eg: 2023-10-26 13:58:22')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
""" if __name__ == '__main__':
    app.run()
 """
# Or specify port manually:
if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5001)
