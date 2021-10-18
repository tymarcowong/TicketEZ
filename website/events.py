from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename
from .forms import CommentForm, EventForm, BookingForm
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
    print(event)
    # create the comment form
    comment_form = CommentForm()

    # # error handling
    if event is None:
        flash(f"Cound not find a destination!", "warning")
        return redirect(url_for("main.index"))

    # return render_template('events/show.html', event=event, form=comment_form, id=id)
    return render_template('events/show.html', form=comment_form, event=event, id=id)


# route to the event create page
@bp.route('/create', methods=['GET', 'POST'])
# @login_required
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
            google_map=event_form.google_map.data,
            description=event_form.description.data,
            image=check_event_img_file(event_form),
            price=event_form.price.data,
            num_tickets=event_form.num_tickers.data,
            # update later once login is implementer
            created_by=2
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()

        flash(f'Successfully created new event', 'success')

        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=event_form, heading="Create Event")

# route for posting comment to the event based on the given ID


@bp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):

    comment_form = CommentForm()
    event_obj = Event.query.filter_by(id=event).first()
    if comment_form.validate_on_submit():

        # POST
        comment = Comment(text=comment_form.text.data,
                          user=current_user,
                          event_id=event_obj,
                          created_at=datetime.now())

        db.session.add(comment)
        db.session.commit()

        # save to database
        flash(f"Comments successfully posted", "success")
    # GET
    return redirect(url_for("events.show", id=event))


@bp.route("<int:id>/update", methods=["GET", "POST"])
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


@bp.route('/<event>/booking', methods=['GET', 'POST'])
def booking():
    booking_form = BookingForm()
    if booking_form.validate_on_submit():
        booking = Booking(booking_form.num_tickets.data)

        db.session.add(booking)
        db.session.commmit()

        flash(f'Booking has been made', 'success')

    return redirect(url_for('events.show', id=booking))
