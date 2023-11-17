#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
import json
import dateutil.parser
import babel
from flask import abort, jsonify, render_template, request, flash
#from markupsafe import Markup
import logging
from logging import Formatter, FileHandler
from forms import *
import sys, time
from models import *
import os
from auth.decorators import AuthError
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




#----------------------------------------------------------------------------#
# TEST CONNECTION AND LOCAL SETUP.
#----------------------------------------------------------------------------#

# test connection and local setup
@app.route("/hello")
def hello():
    return jsonify(
       {
          "greeting": "Hello Mercy"
       }
    ) 




#----------------------------------------------------------------------------#
# HOME or INDEX.
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

#  Show ALL ACTORS
#  ----------------------------------------------------------------
@app.route('/actors')
def actors():

    try:
      actors_list = Actor.query.order_by(Actor.id).all()
      actors = []

      for one_actor in actors_list:
        actor_data = {}
        actor_data['id'] = one_actor.id
        actor_data['name'] = one_actor.name
        actor_data['age'] = one_actor.age
        actor_data['gender'] = one_actor.gender
        actor_data['city'] = one_actor.city
        actor_data['state'] = one_actor.state
        actor_data['genre'] = one_actor.genre
        actor_data['instagram_link'] = one_actor.instagram_link
        actor_data['website_link'] = one_actor.website_link
        actor_data['image_link'] = one_actor.image_link
        actor_data['seeking_casting'] = one_actor.seeking_casting
        actor_data['seeking_description'] = one_actor.seeking_description
        actors.append(actor_data)

      return jsonify(
            {
                "success": True,
                "total_actors": len(actors_list),
                "actors": actors
            }
        )
   
    except Exception as e:
      print(e)
      abort(404)


#  Show ONE ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):

    try:
      actor_selected_data = {}
      actor_selected = Actor.query.get(actor_id)
      showings_joinedwith_movies = Showing.query.filter_by(actor_id=actor_id).join(Movie).all()

      if actor_selected is None:
          abort(404)
      else:
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

    except Exception as e:
      print(e)
      abort(404)
    
    return jsonify(
            {
                "success": True,
                "current_actor_id": actor_id,
                "actor_details": actor_selected_data
            }
        )


#  Create ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/create', methods=['GET'])
def create_actor_form():
    try:
        actor_form = ActorForm()
    except Exception as e:
        print(e)
        abort(404)
    return jsonify(
            {
                "success": True,
                "get_form": True
            }
        )


@app.route('/actors/create', methods=['POST'])
def create_actor_submission():
    actor_name = ''

    try:
      body = request.get_json()
      actor = Actor(name = body.get('name'),
                    age = body.get('age'),
                    gender = body.get('gender'),
                    city = body.get('city'),
                    state = body.get('state'),
                    genre = body.get('genre'),
                    instagram_link = body.get('instagram_link'),
                    website_link = body.get('website_link'),
                    image_link = body.get('image_link'),
                    seeking_casting = body.get('seeking_casting'),
                    seeking_description = body.get('seeking_description')) 
      
      db.session.add(actor)
      db.session.commit()

      actor_name = actor.name
      selection = Actor.query.all()

      return jsonify(
            {
                "success": True,
                "total_actors": len(selection),
                "created_actor_name": actor_name
            }
        )
    
    except Exception as e:
        print(e)
        abort(404)

    finally:
      db.session.close()
    

#  Update ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
    try:
        form = ActorForm()
        actor_to_edit = Actor.query.get(actor_id)

        if actor_to_edit is None:
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

            return jsonify(
                {
                    "success": True,
                    "get_form": True,
                    "actor_id": actor_data['id']
                })

    except Exception as e:
       print(e)
       abort(404)


@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):

    try:
      #actor to edit
      actor_edit = Actor.query.get(actor_id)
      body = request.get_json()

      if actor_edit is None:
        abort(404)
      else:
        actor_edit.name = body.get('name')
        actor_edit.age = body.get('age')
        actor_edit.gender = body.get('gender')
        actor_edit.genre = body.get('genre')
        actor_edit.city = body.get('city')
        actor_edit.state = body.get('state')
        actor_edit.instagram_link = body.get('instagram_link')
        actor_edit.website_link = body.get('website_link')
        actor_edit.image_link = body.get('image_link')
        actor_edit.seeking_casting = body.get('seeking_casting')
        actor_edit.seeking_description = body.get('seeking_description')

        db.session.commit()

    except Exception as e:
      print(e)
      abort(404)
      
    finally:
      db.session.close()

    return jsonify(
       {
          "success": True,
          "actor_id": actor_id
       }
    )
  

#  Delete ACTOR
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/delete', methods=['GET'])
def delete_actor(actor_id):

    try:
        actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor_to_delete is None:
            abort(415)
        else:  
            Actor.query.filter_by(id = actor_id).delete()
            db.session.commit()
            sselection = Actor.query.all()

        return jsonify(
            {
                "success": True,
                "deleted_actor_id": actor_id,
                "total_actors": len(sselection)
            })
    
    except Exception as e:
        print(e)
        abort(404)

    finally:
       db.session.close()
    

    

#  ----------------------------------------------------------------
#  MOVIES
#  ----------------------------------------------------------------


#  Show ALL MOVIES
#  ----------------------------------------------------------------
@app.route('/movies')
def movies():

    try:
        all_movies = Movie.query.order_by(Movie.id).all()
        movie_data = []

        for movie in all_movies:
            movie_formatted = {}
            movie_formatted['id'] = movie.id
            movie_formatted['title'] = movie.title
            movie_formatted['release_date'] = movie.release_date
            movie_formatted['genre'] = movie.genre
            movie_formatted['instagram_link'] = movie.instagram_link
            movie_formatted['website_link'] = movie.website_link
            movie_formatted['image_link'] = movie.image_link
            movie_formatted['seeking_actors'] = movie.seeking_actors
            movie_formatted['seeking_description'] = movie.seeking_description
            movie_data.append(movie_formatted)

        return jsonify(
           {
              "success": True,
              "total_movies": len(all_movies),
              "movies": movie_data
           }
        )

    except Exception as e:
        print(e)
        abort(404)
  

#  Show ONE MOVIE
#  ----------------------------------------------------------------
@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):

    try:
        movie_selected = Movie.query.get(movie_id)
        showings_joinedwith_actors = Showing.query.filter_by(movie_id = movie_id).join(Actor).all()
        
        if movie_selected is None:
           abort(404)

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

            return jsonify(
            {
                "success": True,
                "current_movie_id": movie_id,
                "movie_details": movie_selected_data
            }
            )

    except Exception as e:
      print(e)
      abort(404)


#  Create MOVIE
#  ----------------------------------------------------------------

#2 methods for /movies/create route: get the form, then post the entry
@app.route('/movies/create', methods=['GET'])
def create_movie_form():
    try:
        form = MovieForm()
        return jsonify(
           {
              "success": True,
              "get_form": True
           }
        )
    except Exception as e:
       print(e)
       abort(404)
    

@app.route('/movies/create', methods=['POST'])
def create_movie_submission():
    movie_title = ''

    try: 
        body = request.get_json()
        movie = Movie(title = body.get('title'),
                    release_date = body.get('release_date'),
                    genre = body.get('genre'),
                    website_link = body.get('website_link'),
                    image_link = body.get('image_link'),
                    instagram_link = body.get('instagram_link'),
                    seeking_actors = body.get('seeking_actors'),
                    seeking_description = body.get('seeking_description')) 
      
        movie_title = body.get('title')
        db.session.add(movie)
        db.session.commit()
        selection = Movie.query.all()

        return jsonify(
           {
              "success": True,
              "total_movies": len(selection),
              "new_movie_name": movie_title
           }
        )
    except Exception as e:
        print(e)
        abort(404)
    finally:
        db.session.close()


#  Update MOVIE
#  ----------------------------------------------------------------

# uses 2 methods; edit/get to load preexisting data, and edit/post to post changes made
@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):

    try:
        form = MovieForm()
        movie_to_edit = Movie.query.get(movie_id)
       
        if movie_to_edit is None:
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

            return jsonify(
            {
                "success": True,
                "get_form": True,
                "movie_id": movie_id
            }
            )
    
    except Exception as e:
       print(e)
       abort(404)
  

@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):

    try:
        movie_to_edit = Movie.query.get(movie_id)
        body = request.get_json()

        if movie_to_edit is None:
           abort(404)
        else: 
            movie_to_edit.title = body.get('title')
            movie_to_edit.release_date = body.get('release_date')
            movie_to_edit.genre = body.get('genre')
            movie_to_edit.website_link = body.get('website_link')
            movie_to_edit.image_link = body.get('image_link')
            movie_to_edit.instagram_link = body.get('instagram_link')
            movie_to_edit.seeking_actors = body.get('seeking_actors')
            movie_to_edit.seeking_description = body.get('seeking_description')

            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "movie_id": movie_id
                })

    except Exception as e:
      print(e)
      abort(404)
    finally:
      db.session.close()


#  Delete MOVIE
#  ----------------------------------------------------------------

@app.route('/movies/<int:movie_id>/delete', methods = ['GET'])
def delete_movie(movie_id):

    try:
        movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie_to_delete is None:
            abort(415)

        else:
            Movie.query.filter_by(id = movie_id).delete()
            db.session.commit()
            selection = Movie.query.all()

        return jsonify(
           {
              "success": True,
              "deleted_movie_id": movie_id,
              "total_movies": len(selection)
           }
        )
    
    except Exception as e:
      print(e)
      abort(404)

    finally:
      db.session.close()


#  ----------------------------------------------------------------
#  SHOWINGS
#  ----------------------------------------------------------------

#  Create SHOWING
#  ----------------------------------------------------------------

@app.route('/showings/create', methods=['GET'])
def create_showing_form():
    form = ShowingForm()

    return render_template('forms/new_showing.html', form = form)



@app.route('/showings/create', methods=['POST'])
def create_showing_submission():

    try:
        body = request.get_json()

        showing_created = Showing(actor_id = body.get('actor_id'),
                                  movie_id = body.get('movie_id'),
                                  start_time = body.get('start_time'))
      
        showing_lead_actor_id = body.get('actor_id')

        db.session.add(showing_created)
        db.session.commit()
        selection = Showing.query.all()

        return jsonify(
           {
              "success": True,
              "total_showings": len(selection),
              "showing_lead_actor_id": showing_lead_actor_id
           }
        )

    except Exception as e:
        print(e)
        abort(404)

    finally:
      db.session.close()


#  Show ALL SHOWINGS
#  ----------------------------------------------------------------
@app.route('/showings', methods=['GET'])
def showings():
    try:
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

        return jsonify(
           {
              "success": True,
              "total_showings": len(showings)
           }
        )
    
    except Exception as e:
       print(e)
       abort(404)



# -------------------------------------------------------------------
#  error handlers
# -------------------------------------------------------------------


@app.errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "error": 400,
            "message": "Bad Request",
            "success": False
        }
    )

@app.errorhandler(422)
def unprocessable_entity(error):
    print('***** 422 ERROR ******')
    print(error)

    return jsonify(
        {
            "error": 422,
            "message": "Unprocessable Entity",
            "success": False
        }
    )


@app.errorhandler(404)
def bad_request(error):
    return jsonify(
        {
            "error": 404,
            "message": "Resource Not Found",
            "success": False
        }
    )


@app.errorhandler(415)
def bad_request(error):
    return jsonify(
        {
            "error": 415,
            "message": "Unsupported Media Type",
            "success": False
        }
    )

@app.errorhandler(500)
def bad_request(error):
    return jsonify(
        {
            "error": 500,
            "message": "Internal Server Error",
            "success": False
        }
    )

# -------------------------------------------------------------------
#  error handler for AuthError
# -------------------------------------------------------------------

@app.errorhandler(AuthError)
def auth_error(error):
  print('***** AUTH ERROR ******')
  print(error)

  return jsonify(
    {
      "success": False,
      "error": error.status_code,
      "message": error.error.get('description')
    }
  ), error.status_code


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


