from flask import Blueprint, render_template, request, session, url_for, redirect, flash
from .models import Event

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events_newest = Event.query.order_by(Event.id.desc()).limit(3).all()
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template("index.html", events = events, events_newest = events_newest)


@bp.route('/search')
def search():
    if request.args['search-artist'] is not "" and request.args["search-category"] is "":
        query_string = f"%{request.args['search-artist']}%"
        events = Event.query.filter(Event.artist_name.like(query_string)).order_by(Event.id.desc()).all()
        return render_template('index.html', events=events)

    if request.args['search-artist'] is "" and request.args["search-category"] is not "":
        events = Event.query.filter_by(genre=request.args["search-category"]).order_by(Event.id.desc()).all()
        return render_template('index.html', events=events)
    
    if request.args['search-artist'] is not "" and request.args["search-category"] is not "":
        query_string = f"%{request.args['search-artist']}%"
        events = Event.query.filter(Event.artist_name.like(query_string)).filter_by(genre=request.args["search-category"]).order_by(Event.id.desc()).all()
        return render_template('index.html', events=events)

    return redirect(url_for('main.index'))

    