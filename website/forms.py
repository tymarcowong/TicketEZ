from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateTimeField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILES = ["PNG", "JPG", "png", "jpg", "JPEG", "jpeg"]

# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])


# registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[InputRequired(), Email("Please enter a valid email")])
    contact = IntegerField("Contact Number", validators=[InputRequired('Please enter a valid contact number')])
    address = StringField("Address", validators=[InputRequired('Please enter your address')])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

# create event form
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired()])
    artist_name = StringField('Artist Name', validators=[InputRequired()])
    status = SelectField("Status", choices=[("", "--Please select status--"), ("active", "Active"), ("upcoming", "Upcoming"), ("inactive", "Inactive")])
    genre = SelectField("Genre", choices=[("", "--Please select genre--"), ("country", "Country"), ("electronic", "Electronic"), ("funk", "Funk"), ("hiphop", "Hip Hop"), ("jazz", "Jazz"), ("house", "House"), ("pop", "Pop"), ("rap", "Rap"), ("rock", "Rock")])
    datetime = DateTimeLocalField('Date and Time', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    google_map = StringField('Google Map Link', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILES, message=f'Only supports {ALLOWED_FILES}')])
    price = StringField('Price', validators=[InputRequired()])
    ticket_count = IntegerField("Number of Tickets", validators=[InputRequired()])

# comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Create')
