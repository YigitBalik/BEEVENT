from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SelectField, IntegerField, BooleanField, FloatField, TextAreaField, RadioField
from wtforms import validators
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional, Required
from models import FavoriteList
from services.venue import getCountries, getVenues
from services.event import getStatuses
from services.image import getImages
from datetime import datetime
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=5, max=20, message="The length of the username must be larger than 5 and shorter than 20 characters.")
    ])
    
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=1, max=256, message="The password cannot be empty and length must be shorter than 256 characters.")
    ])
    

class RegisterForm(FlaskForm):
    
    countries_of_venues = getCountries()
    country_choices = [(country,country) for country in countries_of_venues]

    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=5, max=20, message="The length of the username must be larger than 5 and shorter than 20 characters.")
    ])

    email = EmailField("Email", validators=[
        DataRequired(),
        Length(min=1,max=50,message="The email cannot be empty and length must be less 50 characters.")
    ])
    
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=5, max=256, message="The length of the password must be larger than 4 and shorter than 256 characters.")
    ])

    country = SelectField('Country', validators=[DataRequired()], choices=country_choices, validate_choice=False)

    age = IntegerField('Age', validators=[
        DataRequired()
        ])

    admin_request = BooleanField("Admin Request", validators=[
        Optional()
    ])

class EventForm(FlaskForm):
    statuses = getStatuses()

    title = StringField("Title", validators=[
        DataRequired(),
        Length(min=1, max=200,message="The title of the event cannot be empty and length must be less than 200.")
    ])

    genre = StringField("Genre", validators=[
        DataRequired(),
        Length(min=1, max=50, message="The genre cannot be empty and length must be less than 50.")
    ])

    category = StringField("Category", validators=[
        DataRequired(),
        Length(min=1, max=50, message="The category cannot be empty and length must be less than 50.")
    ])

    date = DateField('Date', format='%Y-%m-%d', default = datetime.now(),validators=[
        DataRequired()
        ])

    time = TimeField('Time')

    notCertainTime = BooleanField("Not Certain Time", validators=[
        Optional()
    ])

    price = FloatField('Price',validators=[
        DataRequired()
        ])

    status = SelectField('Status', validators=[DataRequired()], choices=statuses, validate_choice=False)

    Venues = getVenues()
    venues = [(venue.get()['id'],venue.get()['name']) for venue in Venues ]

    venue = SelectField(validators=[DataRequired()], choices=venues, validate_choice=False)

    Images = getImages()
    images = [(image.get()['id'], image.get()['alt']) for image in Images]

    image = SelectField(validators=[DataRequired()], choices=images, validate_choice=False)

class ImageForm(FlaskForm):
    height = IntegerField('Height', validators=[
        DataRequired()
        ])

    width = IntegerField('Width', validators=[
        DataRequired()
        ])

    source = StringField("Source", validators=[
        DataRequired(),
        Length(min=1, max=150, message="The Source cannot be empty and length must be less than 150.")
    ])
    
    alt = StringField("Alt", validators=[
        DataRequired(),
        Length(min=1, max=200, message="The alt text cannot be empty and length must be less than 200.")
    ])

class VenueForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=5, max=100, message="The length of the venue name must be larger than 5 and shorter than 100 characters.")
        ])

    city = StringField("City", validators=[
        DataRequired(),
        Length(min=5, max=50, message="The length of the city name must be larger than 5 and shorter than 50 characters.")
        ])

    country = StringField("Country", validators=[
        DataRequired(),
        Length(min=5, max=100, message="The length of the country name must be larger than 5 and shorter than 100 characters.")
        ])

    address = TextAreaField("Adress", validators=[
        DataRequired(),
        Length(min=5, max = 100,  message="The length of the address must be larger than 5 and shorter than 100 characters.")
        ])

    timezone = StringField("Timezone", validators=[
        DataRequired(),
        Length(min=5, max=50, message="The length of the timezone must be larger than 5 and shorter than 50 characters.")
        ])

class UploadFile(FlaskForm):
    file = FileField(validators=[DataRequired()])

class UpdateUserForm(FlaskForm):
    
    countries_of_venues = getCountries()
    country_choices = [(country,country) for country in countries_of_venues]

    username = StringField("Username", validators=[
        Length(min=5, max=20, message="The length of the username must be larger than 5 and shorter than 20 characters.")
    ])

    email = EmailField("Email", validators=[
        Length(min=1,max=50,message="The email cannot be empty and length must be less 50 characters.")
    ])
    
    country = SelectField('Country', choices=country_choices, validate_choice=False)

    age = IntegerField('Age')

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
        Length(min=5, max=256, message="The length of the password must be larger than 4 and shorter than 256 characters.")
    ])

#Evaluation
class AddEvaluationForm(FlaskForm):
    
    comment = TextAreaField("Comment", validators=[
        Length(min=5, max=200, message="The length of the comment must be larger than 5 and shorter than 200 characters.")
    ])

    priceRate = RadioField("Price Rate", choices=[1,2,3,4,5])

    funRate = RadioField("Fun Rate", choices=[1,2,3,4,5])

#FavoriteList
class CreateFavoriteListForm(FlaskForm):
    
    list_name = StringField("List Name", validators=[
        Length(min=5, max=80, message="The length of the name must be larger than 5 and shorter than 80 characters."),DataRequired()
    ])

    description = StringField("Description", validators=[
        Length(min=5, max=300, message="The length of the description must be larger than 5 and shorter than 300 characters.")
    ])

    public = RadioField("Visible by others", validators=[DataRequired()],choices=["yes","no"]) 