from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField
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
    event_status = StringField('Event Status', validators=[InputRequired()])
    event_genre = StringField('Event Genre', validators=[InputRequired()])
    date = StringField('Date', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    google_map = TextAreaField('Google Map', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILES, message='Only supports png,jpg,JPG,PNG')])
    Price = StringField('Price', validators=[InputRequired()])
    submit = SubmitField("Create")

# comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Create')
