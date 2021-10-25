from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename
from .forms import CommentForm, EventForm, BookingForm, EventEditForm
from .models import Event, Comment, Booking


# from .models import Destination, Comment
# from .forms import DestinationForm, CommentForm

bp = Blueprint('event', __name__, url_prefix='/events')

EVENT_GENRES = ["Country", "Electronic", "Funk",
                "Hip Hop", "Jazz", "House", "Pop", "Rap", "Rock"]

# route for events based on the ID provided form the URL


@bp.route('/<int:id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    comment_form = CommentForm()
    booking_form = BookingForm()
    # # error handling
    if event is None:
        flash(f"Cound not find a destination!", "warning")
        return redirect(url_for("main.index"))

    # return render_template('events/show.html', event=event, form=comment_form, id=id)
    return render_template('events/show.html', comment_form=comment_form, booking_form=booking_form, 
        event=event, id=id, display_edit_button = login_user_is_creator(current_user, event.created_by))


# route to the event create page
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(
            event_name=event_form.event_name.data,
            artist_name=event_form.artist_name.data,
            status=event_form.status.data,
            genre=event_form.genre.data,
            # update datetime format later
            # date = event_form.datetime.data,
            date=datetime(2021, 10, 16),
            location=event_form.location.data,
            description=event_form.description.data,
            image=check_event_img_file(event_form),
            price=event_form.price.data,
            num_tickets=event_form.num_tickers.data,
            created_by=current_user.id,
            google_map="k"
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()

        flash(f'Successfully created new event', 'success')

        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=event_form, heading="Create Event")


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = Event.query.filter_by(id=id).first()
    if login_user_is_creator(current_user, event.created_by) == False:
        flash(f'You must be the creator of the event to edit the details!', 'warning')
        return redirect(url_for('event.show', id=event.id))
    
   
    event_edit_form = EventEditForm()
    if event_edit_form.validate_on_submit():
        if event_edit_form.event_name.data != "":
            event.event_name = event_edit_form.event_name.data
        if event_edit_form.artist_name.data != "":
            event.artist_name = event_edit_form.artist_name.data
        if event_edit_form.status.data != "":
            event.status = event_edit_form.status.data
        if event_edit_form.genre.data != "":
            event.genre = event_edit_form.genre.data
        if event_edit_form.datetime.data != "":
        #  update datetime format later
        #  date = event_edit_form.datetime.data,
            event.date = datetime(2021, 10, 16)
        if event_edit_form.location.data != "":
            event.location = event_edit_form.location.data
        if event_edit_form.description.data != "":
            event.description = event_edit_form.description.data
        if event_edit_form.image.data is not None:
            event.image = check_event_img_file(event_edit_form)
        if event_edit_form.price.data is not None:
            event.price = event_edit_form.price.data
        if event_edit_form.num_tickers.data is not None :
            event.num_tickets = event_edit_form.num_tickers.data

        # commit to the database
        db.session.commit()

        flash(f'Successfully updated event details', 'success')

        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=event_edit_form, heading="Create Event")


@bp.route('/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        # POST
        comment = Comment(text = comment_form.text.data,
                          # change user id after login function is implemented - Marco
                          user_id = current_user.id,
                          event_id = id,
                          posted_at = datetime.now())

        db.session.add(comment)
        db.session.commit()
        # save to database
        flash(f"Comments successfully posted", "success")
    # GET
    return redirect(url_for("event.show", id=id))



@bp.route('/<int:id>/booking', methods=['GET', 'POST'])
@login_required
def booking(id):
    booking_form = BookingForm()
    if booking_form.validate_on_submit():
        booking = Booking(
            num_tickets = booking_form.num_tickets.data,
            user_id = current_user.id,
            event_id = id)
        db.session.add(booking)
        db.session.commit()
        flash(f'Booking has been made', 'success')
    return redirect(url_for('event.show', id=id))


def check_event_img_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    EVENT_IMG_PATH = "static/img/events/"
    upload_path = os.path.join(
        BASE_PATH, EVENT_IMG_PATH, secure_filename(filename))
    db_upload_path = EVENT_IMG_PATH + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


def login_user_is_creator(login_user, creator_id):
    try:
        return login_user.id == creator_id
    except:
        return False
    
