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

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. == DONE
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue. == DONE

  cities_list = Venue.query.distinct('city')
  areas = []

  for one_city in cities_list:
    city_data = {}
    city_data['city'] = one_city.city
    city_data['state'] = one_city.state
    city_data['venues'] = Venue.query.filter_by(city = one_city.city)
    city_data['num_upcoming_shows'] = Show.query.filter_by(venue_id = one_city.id).count()
    areas.append(city_data)

  return render_template('pages/venues.html', areas=areas)

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


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id == DONE

  error = False

  try:
    venue_selected_data = {}
    venue_selected = Venue.query.get(venue_id)
    shows_joinedwith_artists = Show.query.filter_by(venue_id = venue_id).join(Artist).all()

    venue_selected_data['id'] = venue_selected.id
    venue_selected_data['name'] = venue_selected.name
    venue_selected_data['genres'] = venue_selected.genres
    venue_selected_data['address'] = venue_selected.address
    venue_selected_data['city'] = venue_selected.city
    venue_selected_data['state'] = venue_selected.state
    venue_selected_data['phone'] = venue_selected.phone
    venue_selected_data['website'] = venue_selected.website_link
    venue_selected_data['facebook_link'] = venue_selected.facebook_link
    venue_selected_data['seeking_talent'] = venue_selected.seeking_talent
    venue_selected_data['seeking_description'] = venue_selected.seeking_description
    venue_selected_data['image_link'] = venue_selected.image_link
    venue_selected_data['past_shows'] = []
    venue_selected_data['upcoming_shows'] = []
    venue_selected_data['past_shows_count'] = 0
    venue_selected_data['upcoming_shows_count'] = 0

    #traverse the Show+Artist data to retrieve the artist details from past shows and upcoming shows
    for show in shows_joinedwith_artists:
      this_show = {}
      this_show['artist_id'] = show.artist_id
      this_show['artist_name'] = show.artist.name
      this_show['artist_image_link'] = show.artist.image_link
      this_show['start_time'] = show.start_time

      #get current timestamp and convert timestamp from db, then compare to populate past shows and upcoming shows
      show_start_time = show.start_time
      show_start_time_formatted = datetime.strptime(show_start_time, '%Y-%m-%d %H:%M:%S')
      db_timestamp = datetime.timestamp(show_start_time_formatted)
      current_timestamp = time.time()

      if current_timestamp > db_timestamp:
        venue_selected_data['past_shows'].append(this_show)
        venue_selected_data['past_shows_count'] += 1
      else:
        venue_selected_data['upcoming_shows'].append(this_show)
        venue_selected_data['upcoming_shows_count'] += 1
  except:
    error = True
    print(sys.exc_info())
  if error:
    error = False
    flash('This venue does NOT exist in our records.')
    abort(404)
  
  return render_template('pages/show_venue.html', venue=venue_selected_data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead == DONE
  error = False
  venueName = ''
  data = {}

  try:
    #leverage the WTForm wrappers
    form = VenueForm(request.form)

    venue = Venue(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  address = form.address.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  image_link = form.image_link.data,
                  facebook_link = form.facebook_link.data,
                  website_link = form.website_link.data,
                  seeking_talent = form.seeking_talent.data,
                  seeking_description = form.seeking_description.data)
    db.session.add(venue)
    db.session.commit()

    venueName = form.name.data

    data['id'] = venue.id
    data['name'] = venue.name
    data['city'] = venue.city
    data['state'] = venue.state
    data['address'] = venue.address
    data['phone'] = venue.phone
    data['genres'] = venue.genres
    data['image_link'] = venue.image_link
    data['facebook_link'] = venue.facebook_link
    data['website_link'] = venue.website_link
    data['seeking_talent'] = venue.seeking_talent
    data['seeking_description'] = venue.seeking_description
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    error = False
    print('data to input:: ')
    print(data)
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead. == DONE
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + venueName + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
    # on successful db insert, flash success
    print(data)
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # TODO: modify data to be the data object returned from db insertion == DONE
  return render_template('pages/home.html', venues=data)


@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using == DONE
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that == DONE
  # clicking that button delete it from the db then redirect the user to the homepage

  error = False
  
  try:
    Venue.query.filter_by(id = venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    flash('Venue successfully deleted!')
  if error:
    error = False
    flash('An error occured. Venue could NOT be deleted.')
    abort(404)
 
  return redirect(url_for('index'))


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
