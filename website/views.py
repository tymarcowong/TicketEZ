from flask import Blueprint, render_template, request, session, url_for, redirect

bp = Blueprint('main', __name__)

# base route
@bp.route('/')
def index():
    return render_template("index.html")