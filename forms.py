from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, ValidationError
import re
from wtforms.validators import DataRequired, URL

def validate_phone(form, phone):
    us_phone_num = '^([0-9]{3}[-][0-9]{3}[-][0-9]{4}$)'
    match = re.search(us_phone_num, phone.data)
    if not match:
        raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')


class ShowingForm(Form):
    actor_id = StringField(
        'actor_id',
        validators=[DataRequired()]
    )
    actor_id_2 = StringField(
        'actor_id_2',
        validators=[DataRequired()]
    )
    movie_id = StringField(
        'movie_id',
        validators=[DataRequired()]
    )
    start_time = StringField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    gender = StringField(
        'gender'
    )
    genre = SelectMultipleField(
        # TODO implement enum restriction
        'genre', validators=[DataRequired()],
        choices=[
            ('Action', 'Action'),
            ('Adventure', 'Adventure'),
            ('Animation', 'Animation'),
            ('Comedy', 'Comedy'),
            ('Crime', 'Crime'),
            ('Drama', 'Drama'),
            ('Fantasy', 'Fantasy'),
            ('History', 'History'),
            ('Melodrama', 'Melodrama'),
            ('Mystery', 'Mystery'),
            ('Narrative', 'Narrative'),
            ('Romance', 'Romance'),
            ('Science Fiction', 'Science Fiction'),
            ('Sports', 'Sports'),
            ('Thriller', 'Thriller'),
            ('War', 'War'),
            ('Other', 'Other'),
        ]
    )
    instagram_link = StringField(
        'instagram_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )
    image_link = StringField(
        'image_link'
    )
    seeking_casting = BooleanField( 
        'seeking_casting' 
    )
    seeking_description = StringField(
        'seeking_description'
    )


class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    release_date = StringField(
        'release_date',
        validators=[DataRequired()],
        default= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    genre = SelectMultipleField(
        # TODO implement enum restriction
        'genre', validators=[DataRequired()],
        choices=[
            ('Action', 'Action'),
            ('Adventure', 'Adventure'),
            ('Animation', 'Animation'),
            ('Comedy', 'Comedy'),
            ('Crime', 'Crime'),
            ('Drama', 'Drama'),
            ('Fantasy', 'Fantasy'),
            ('History', 'History'),
            ('Melodrama', 'Melodrama'),
            ('Mystery', 'Mystery'),
            ('Narrative', 'Narrative'),
            ('Romance', 'Romance'),
            ('Science Fiction', 'Science Fiction'),
            ('Sports', 'Sports'),
            ('Thriller', 'Thriller'),
            ('War', 'War'),
            ('Other', 'Other'),
        ]
    )
    instagram_link = StringField(
        'instagram_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )
    image_link = StringField(
        'image_link'
    )
    seeking_actors = BooleanField( 
        'seeking_actors' 
    )
    seeking_description = StringField(
        'seeking_description'
    )
