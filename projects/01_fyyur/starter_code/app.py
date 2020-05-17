#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
#                       !!!!!WARNING!!!!!
#
#                     change genres1 To genres 
#                 why i changed? beceuse altra felid to array 
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#finsh in config app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/fyyur'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
  __tablename__ = 'Venue'
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(500))
  seeking_talent =  db.Column(db.Boolean, nullable=True, default=False)
  seeking_description = db.Column(db.String(120))
  genres1 = db.Column(ARRAY(db.String(120)))
  
  

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres1 = db.Column(ARRAY(db.String(120)))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  website = db.Column(db.String(500))
  seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
  seeking_description = db.Column(db.String(120))
  

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)   
  venue_name = db.relationship('Venue', backref=db.backref('Shows'))
  artist = db.relationship('Artist', backref=db.backref('shows'))

db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
      format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  venues_list = Venue.query.all()
  city_state = set()
  for venue in venues_list:
    city_state.add((venue.city, venue.state))

  
  for location in city_state:
    data.append({
        "city": location[0],
        "state": location[1],
        "venues": []
    })

  for venue in venues_list:
    num_upcoming_shows = 0

    shows = Show.query.filter_by(venue_id=venue.id).all()
    current_date = datetime.now()

    for show in shows:
      if show.start_time > current_date:
          num_upcoming_shows += 1

    for venue_location in data:
      if venue.state == venue_location['state'] and venue.city == venue_location['city']:
        venue_location['venues'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })
        
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term= request.form.get('search_term', '')
  res =Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  response={
    "count": res.count(),
    "data": res
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={}
  venue = Venue.query.get(venue_id)
  shows_id = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
<<<<<<< HEAD
  upcom_shows = []
=======
  upcoming_shows = []
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
  current_time = datetime.now()
  for show in shows_id:
    data1={
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
        } 
    if show.start_time > current_time:
<<<<<<< HEAD
      upcom_shows.append(data1)
=======
      upcoming_shows.append(data1)
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
    else:
      past_shows.append(data1)
    data1={
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres1,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
     "seeking_description":venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
<<<<<<< HEAD
      "upcoming_shows": upcom_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcom_shows)
=======
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
  }

  return render_template('pages/show_venue.html', venue=data1);

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  #  insert form data as a new Venue record in the db, instead
  #  modify data to be the data object returned from db insertion
  try:
    form = VenueForm(request.form)
    data = Venue(
    name = form.name.data,
    genres1 = form.genres.data,
    address = form.address.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_talent = form.seeking_talent.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data,
  )
    db.session.add(data)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  except:
    # on unsuccessful db insert, flash an error instead
    db.session.rollback()
    flash('An error occurred. Venue ' + data.name + ' could not be listed. ')
    flash(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE', 'GET'])
def delete_venue(venue_id):
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  ### conspt right but l don't know why don't delete button WORK

  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue  was successfully DELETE!')
    flash(sys.exc_info())
  except:
    db.session.rollback()
    flash(sys.exc_info())
    flash('An error occurred. Venue could not be DELETE.')
  finally:
    flash(sys.exc_info())

    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  data=[]
  artists= Artist.query.all()
  for artist in artists:
    data.append({
      'id': artist.id,
      'name':artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term= request.form.get('search_term', '')
  res =Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response={
    "count": res.count(),
    "data": res
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={}
  artist = Artist.query.get(artist_id)
  shows_id = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
<<<<<<< HEAD
  upcom_shows = []
=======
  upcoming_shows = []
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
  current_time = datetime.now()
  for show in shows_id:
    data1={
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
        } 
    if show.start_time > current_time:
<<<<<<< HEAD
      upcom_shows.append(data1)
=======
      upcoming_shows.append(data1)
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
    else:
      past_shows.append(data1)
    data1={
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres1,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_talent": artist.seeking_talent,
     "seeking_description":artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_shows,
<<<<<<< HEAD
      "upcoming_shows": upcom_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcom_shows)
=======
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
>>>>>>> 9bb9bbe976418b253a5e3d4b68801a233bb3537c
  }
  return render_template('pages/show_artist.html', artist=data1)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres1,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  try:
    artist.name = form.name.data
    artist.phone = form.phone.data
    artist.state = form.state.data
    artist.city = form.city.data
    artist.genres1 = form.genres.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_description= form.seeking_description.data
    artist.seeking_talent = form.seeking_talent.data
    artist.website= form.website.data
    db.session.commit()
    flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
  except:
    db.session.rollback()
    flash(sys.exc_info())
    flash('An error occurred. Artist could not be updated.')
  finally:
    flash(sys.exc_info())
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue1 = Venue.query.get(venue_id)
  venue={
    "id": venue1.id,
    "name": venue1.name,
    "genres": venue1.genres1,
    "address": venue1.address,
    "city": venue1.city,
    "state": venue1.state,
    "phone": venue1.phone,
    "website": venue1.website,
    "facebook_link": venue1.facebook_link,
    "seeking_talent": venue1.seeking_talent,
    "seeking_description": venue1.seeking_description,
    "image_link": venue1.image_link,
    }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST','GET'])
def edit_venue_submission(venue_id):
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  try:
    name = form.name.data
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
    flash('Venue has been updated')
  except:
    db.session.rollback()
    flash(sys.exc_info())
    flash('An error occurred. Artist could not be updated.')
  finally:
    flash(sys.exc_info())
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  # called upon submitting the new artist listing form
  # insert form data as a new Venue record in the db, instead
  #modify data to be the data object returned from db insertion
  try:
    artist = Artist(
      name=form.name.data, 
      city=form.city.data, 
      state=form.city.data,
      phone=form.phone.data,
      genres1=form.genres.data, 
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      seeking_description= form.seeking_description.data,
      seeking_talent = form.seeking_talent.data,
      website= form.website.data
    )
    
    db.session.add(artist)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except: 
  #  unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash(sys.exc_info())
    flash('An error occurred. Artist could not be listed.')
  finally:
    flash(sys.exc_info())
    db.session.close()
    flash('An error occurred. Artist  could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  shows = Show.query.order_by(db.desc(Show.start_time))
  for show in shows:
    artists=Artist.query.get(show.artist_id)
    venues=Venue.query.get(show.venue_id)
    data.append({
        "venue_id": show.venue_id,
        "venue_name": venues.name,
        "artist_id": show.artist_id,
        "artist_name": artists.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  #  insert form data as a new Show record in the db, instead
  try:
    show= Show(
      artist_id=request.form['artist_id'],
      venue_id=request.form['venue_id'],
      start_time=request.form['start_time']
    )
    db.session.add(show)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash(sys.exc_info())
    flash('An error occurred. Artist could not be listed.')
  finally:
    flash(sys.exc_info())
    db.session.close()
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
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
