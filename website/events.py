from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from . import db
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename

# from .models import Destination, Comment
# from .forms import DestinationForm, CommentForm

bp = Blueprint('event', __name__, url_prefix='/events')

# route for events based on the ID provided form the URL
@bp.route('/<int:id>')
def show(id):
    # destination = Destination.query.filter_by(id=id).first()
    # # create the comment form
    # comment_form = CommentForm()    

    # # error handling 
    # if destination is None:
    #   flash(f"Cound not find a destination!", "warning")
    #   return redirect(url_for("main.index"))
    # return render_template('events/show.html', destination=destination, form=comment_form, id=id)
    return render_template('events/show.html')

# route to the event create page
@bp.route('/create', methods = ['GET', 'POST'])
def create():
#   form = DestinationForm()
#   if form.validate_on_submit():
#     destination = Destination(
#       name = form.name.data,
#       description = form.description.data,
#       image = check_upload_file(form),
#       currency = form.currency.data
#     )    
#     # add the object to the db session
#     db.session.add(destination)
#     # commit to the database
#     db.session.commit()

#     flash(f'Successfully created new travel destination', 'success')

#     return redirect(url_for('destination.show', id=destination.id)) 
#   return render_template('events/create.html', form=form)
  return render_template('events/create.html')

# route for posting comment to the event based on the given ID
@bp.route('/<int:id>/comment', methods = ['GET', 'POST'])  
# def comment(id):  
#     form = CommentForm()  
#     if form.validate_on_submit():
#       # POST
#       comment = Comment(
#         text = form.text.data,
#         user_id = 1,
#         destination_id = id,
#         created_at = datetime.now()
#       )

#       db.session.add(comment) 
#       db.session.commit()
      
#       # save to database
#       flash(f"Comments successfully posted","success")

#     # GET
#     return redirect(url_for("destination.show", id=id))

@bp.route("<int:id>/update", methods = ["GET", "POST"])

def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, "static/images/", secure_filename(filename))
  db_upload_path="static/images/"+secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path