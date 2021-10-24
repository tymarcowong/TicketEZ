from flask import Blueprint, render_template, request, session, url_for, redirect
from .models import Event

bp = Blueprint('main', __name__)

# base route
@bp.route('/')
def index():
    events_newest = Event.query.order_by(Event.id.desc()).limit(3).all()
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template("index.html", events = events, events_newest = events_newest)