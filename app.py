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
from forms import *
import sys, time
from models import *
import os
from auth.decorators import requires_auth, AuthError
#----------------------------------------------------------------------------#
# App Config.
# NOTE: Refactored to file models.py == DONE

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

#  ----------------------------------------------------------------
#  HOME or INDEX
#  ----------------------------------------------------------------

@app.route('/')
def index():
  excited = os.environ['EXCITED']
  if excited == 'true':
    print("***EXCITED is true!!********")
  #token = get_token_auth_header()
  #session['user'] = token
  return render_template('pages/home.html')


#  ----------------------------------------------------------------
#  ACTORS
#  ----------------------------------------------------------------


#  Show ALL ACTORS
#  ----------------------------------------------------------------
@app.route('/actors')
@requires_auth('get:actors')
def actors(payload):
  if 'get:actors' in payload['permissions']:
    print('**** payload /actors *****')
    print(payload['permissions'])

    try:
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
    
    except Exception as e:
      print(e)
      abort(404)

  else:
    abort(AuthError)
  

#  Show ONE ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>')
@requires_auth('get:actors')
def show_actor(payload, actor_id):
  if 'get:actors' in payload['permissions']:
    print('****payload /actors/ID*****')
    print(payload['permissions'])

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
        this_showing['movie_id'] = showing.movie.id
        this_showing['movie_title'] = showing.movie.title
        this_showing['movie_image_link'] = showing.movie.image_link

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

      return render_template('pages/show_actor.html', actor=actor_selected_data)

    except:
      error = True
      print(sys.exc_info())

    if error:
      error = False
      flash('This actor does NOT exist in our records.')
      return render_template('pages/home.html')
    
  else:
    abort(AuthError)


#  Create ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/create', methods=['GET'])
@requires_auth('post:actors')
def create_actor_form(payload):
  if 'post:actors' in payload['permissions']:
    print('**** payload /actors/create GET FORM *****')
    print(payload['permissions'])
    
    actor_form = ActorForm()
    return render_template('forms/new_actor.html', form=actor_form)
  else:
    abort(AuthError)


@app.route('/actors/create', methods=['POST'])
@requires_auth('post:actors')
def create_actor_submission(payload):
  if 'post:actors' in payload['permissions']:
    print('**** payload /actors/create POST FORM *****')
    print(payload['permissions'])

    error = False
    actor_name = ''

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
  
  else:
    abort(AuthError)


#  Update ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
@requires_auth('patch:actors')
def edit_actor(payload, actor_id):
  if 'patch:actors' in payload['permissions']:
    print('**** payload /actors/ID/edit GET FORM *****')
    print(payload['permissions'])

    form = ActorForm()
    actor_to_edit = Actor.query.get(actor_id)

    if actor_to_edit is None:
      flash('An error occured. Actor not found in our records.')
      abort(404)
    else:
      actor_data = {}

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

      return render_template('/forms/edit_actor.html', form = form, actor = actor_data)
  
  else:
    abort(AuthError)


@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
@requires_auth('patch:actors')
def edit_actor_submission(payload, actor_id):
  if 'patch:actors' in payload['permissions']:
    print('**** payload /actors/ID/edit POST FORM *****')
    print(payload['permissions'])

    error = False
    form = ActorForm(request.form)
    actor_edit = Actor.query.filter(Actor.id == actor_id).one_or_none()

    try:
      if actor_edit is None:
        flash('An error occured. Actor not found in our records.')
        abort(404)
      else:
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

        db.session.commit()
        flash('Edit was successful!')

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

    return redirect(url_for('show_actor', actor_id = actor_id))
  
  else:
    abort(AuthError)


#  Delete ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/delete', methods=['GET'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
  if 'delete:actors' in payload['permissions']:
    print('**** payload /actors/ID/delete *****')
    print(payload['permissions'])

    error = False
    actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

    try:
      if actor_to_delete is None:
        flash('An error occured. Actor not found in our records.')
        abort(404)
        #check error 415 if URL is http://127.0.0.1:5001/actors/44000/delete
      else:
        Actor.query.filter_by(id = actor_id).delete()
        db.session.commit()
        flash('Actor successfully deleted!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      error = False
      flash('An error occured. Actor not deleted.')
      abort(404)
    
    return redirect(url_for('index'))
  
  else:
    abort(AuthError)




#  ----------------------------------------------------------------
#  MOVIES
#  ----------------------------------------------------------------


#  Show ALL MOVIES
#  ----------------------------------------------------------------
@app.route('/movies')
@requires_auth('get:movies')
def movies(payload):
  if 'get:movies' in payload['permissions']:
    print('**** payload /movies *****')
    print(payload['permissions'])

    try:
      all_movies = Movie.query.all()
      movie_data = []

      for movie in all_movies:
        movie_formatted = {}
        movie_formatted['id'] = movie.id
        movie_formatted['title'] = movie.title
        movie_data.append(movie_formatted)

      return render_template('pages/movies.html', movies = movie_data)
    
    except Exception as e:
      print(e)
      abort(404)
  
  else:
    abort(AuthError)


#  Show ONE MOVIE
#  ----------------------------------------------------------------
@app.route('/movies/<int:movie_id>')
@requires_auth('get:movies')
def show_movie(payload, movie_id):
  if 'get:movies' in payload['permissions']:
    print('**** payload /movies/ID *****')
    print(payload['permissions'])

    error = False

    try:
      movie_selected = Movie.query.get(movie_id)
      showings_joinedwith_actors = Showing.query.filter_by(movie_id = movie_id).join(Actor).all()
      
      if movie_selected is None:
        flash('This Movie does NOT exist in our records.')
        error = True
        #confirm this on the browser
      else: 
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
  
  else:
    abort(AuthError)


#  Create MOVIE
#  ----------------------------------------------------------------

#2 methods for /movies/create route: get the form, then post the entry
@app.route('/movies/create', methods=['GET'])
@requires_auth('post:movies')
def create_movie_form(payload):
  if 'post:movies' in payload['permissions']:
    print('**** payload /movies/create GET FORM *****')
    print(payload['permissions'])

    form = MovieForm()

    return render_template('forms/new_movie.html', form = form)
  
  else:
    abort(AuthError)


@app.route('/movies/create', methods=['POST'])
@requires_auth('post:movies')
def create_movie_submission(payload):
  if 'post:movies' in payload['permissions']:
    print('**** payload /movies/create POST FORM *****')
    print(payload['permissions'])

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
  
  else:
    abort(AuthError)


#  Update MOVIE
#  ----------------------------------------------------------------

# uses 2 methods; edit/get to load preexisting data, and edit/post to post changes made
@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
@requires_auth('patch:movies')
def edit_movie(payload, movie_id):
  if 'patch:movies' in payload['permissions']:
    print('**** payload /movies/ID/edit FORM GET *****')
    print(payload['permissions'])

    form = MovieForm()
    movie_to_edit = Movie.query.get(movie_id)

    if movie_to_edit is None:
      flash('An error occured. Movie not found in our records.')
      abort(404)
    else:
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
      form.release_date.data = movie_to_edit.release_date
      form.genre.data = movie_to_edit.genre
      form.website_link.data = movie_to_edit.website_link
      form.image_link.data = movie_to_edit.image_link
      form.instagram_link.data = movie_to_edit.instagram_link
      form.seeking_actors.data = movie_to_edit.seeking_actors
      form.seeking_description.data = movie_to_edit.seeking_description

      return render_template('forms/edit_movie.html', form=form, movie=movie_data)
  
  else:
    abort(AuthError)


@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
@requires_auth('patch:movies')
def edit_movie_submission(payload, movie_id):
  if 'patch:movies' in payload['permissions']:
    print('**** payload /movies/ID/edit FORM POST *****')
    print(payload['permissions'])

    error = False
    form = MovieForm(request.form)
    movie_to_edit = Movie.query.filter(Movie.id == movie_id).one_or_none()

    try:
      if movie_to_edit is None:
        flash('An error occured. Movie not found in our records.')
        abort(404)
      else:
        movie_to_edit.title = form.title.data
        movie_to_edit.release_date = form.release_date.data
        movie_to_edit.genre = form.genre.data
        movie_to_edit.website_link = form.website_link.data
        movie_to_edit.image_link = form.image_link.data
        movie_to_edit.instagram_link = form.instagram_link.data
        movie_to_edit.seeking_actors = form.seeking_actors.data
        movie_to_edit.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Edit was successfull!')

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

    return redirect(url_for('show_movie', movie_id = movie_id))
  
  else:
    abort(AuthError)



#  Delete MOVIE
#  ----------------------------------------------------------------

@app.route('/movies/<int:movie_id>/delete', methods = ['GET'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
  if 'delete:movies' in payload['permissions']:
    print('**** payload /movies/ID/delete *****')
    print(payload['permissions'])

    error = False
    
    try:
      movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie_to_delete is None:
        flash('An error occured. Movie not found in our records.')
        abort(404)
        #check error 415 if URL is http://127.0.0.1:5001/movies/44000/delete
      else:
        Movie.query.filter_by(id = movie_id).delete()
        db.session.commit()
        flash('Movie successfully deleted.')

    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

    finally:
      db.session.close()

    if error:
      error = False
      flash('An error occured. Actor not deleted.')
      abort(404)
    
    return render_template('pages/home.html')
  
  else:
    abort(AuthError)


#  ----------------------------------------------------------------
#  SHOWINGS
#  ----------------------------------------------------------------

#  Create SHOWING
#  ----------------------------------------------------------------

@app.route('/showings/create', methods=['GET'])
@requires_auth('post:showings')
def create_showing_form(payload):
  if 'post:showings' in payload['permissions']:
    print('**** payload /showings/create GET FORM *****')
    print(payload['permissions'])
    form = ShowingForm()

    return render_template('forms/new_showing.html', form = form)
  
  else:
    abort(AuthError)


@app.route('/showings/create', methods=['POST'])
@requires_auth('post:showings')
def create_showing_submission(payload):
  if 'post:showings' in payload['permissions']:
    print('**** payload /showings/create POST FORM *****')
    print(payload['permissions'])

    error = False

    try:
      form = ShowingForm(request.form)

      showing_created = Showing(actor_id = form.actor_id.data,
                                movie_id = form.movie_id.data,
                                start_time = form.start_time.data)
      
      db.session.add(showing_created)
      db.session.commit()
      flash('Showing successfully added!')

    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

    finally:
      db.session.close()
      

    if error:
      error = False
      flash('An error occured. Showing NOT created.')

    return render_template('pages/home.html')
  
  else:
    abort(AuthError)


#  Show ALL SHOWINGS
#  ----------------------------------------------------------------
@app.route('/showings', methods=['GET'])
@requires_auth('get:showings')
def showings(payload):
  if 'get:showings' in payload['permissions']:
    print('**** payload deeeets /showings *****')
    print(payload['permissions'])

    showings = Showing.query.order_by(Showing.id).all()

    all_showings = []

    for showing in showings:
      this_showing = {}
      movie_details = Movie.query.filter_by(id = showing.movie_id).one_or_none()
      actor_details = Actor.query.filter_by(id = showing.actor_id).one_or_none()

      this_showing['id'] = showing.id
      this_showing['actor_id'] = showing.actor_id
      this_showing['movie_id'] = showing.movie_id
      this_showing['start_time'] = showing.start_time
      this_showing['movie_title'] = movie_details.title
      this_showing['actor_name'] = actor_details.name
      this_showing['movie_image_link'] = movie_details.image_link

      all_showings.append(this_showing)

    return render_template('pages/showings.html', showings = all_showings)
  
  else:
    abort(AuthError)




# -------------------------------------------------------------------
# ERROR HANDLERS
# -------------------------------------------------------------------


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(AuthError)
def auth_error(error):
    print('***** AUTH ERROR ******')
    print(error)

    error_details = {}

    error_details['success'] = False
    error_details['error'] = error.status_code
    error_details['message'] = error.error.get('description')
    error_details['developer_code'] = error.error.get('code')

    return render_template('errors/autherror.html', error_details = error_details)



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


