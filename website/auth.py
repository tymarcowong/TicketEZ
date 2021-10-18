from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db
from .models import User

from pprint import pprint


#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        #POST
        # get data from form
        username = login_form.user_name.data
        password = login_form.password.data
        # check is user exists in the database
        check_user = User.query.filter_by(name = username).first()
        # if user exists, check is password is correct
        if check_user is not None:
            if check_password_hash(check_user.password_hash, password):
                # user name and password are correct
                
                # login_user(check_user)
                flash(f"Welcome, {check_user.name}!", "success")
                return redirect(url_for("main.index"))
        flash(f"Incorrect credentials!", "warning")

    #GET
    return render_template("user.html", heading="Login", form=login_form)
    

@bp.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        # POST
        # get data from the from
        username = register_form.user_name.data
        contact_number = register_form.contact.data
        address = register_form.address.data
        email = register_form.email_id.data
        password = register_form.password.data

        # get if data already exists in database
        check_user = User.query.filter_by(name=username).first()
        if check_user is None:
            # User does not exist in the database
            # create and commit user to the database
            new_user = User(
                name = username,
                email_id = email,
                contact_number = contact_number,
                address = address,
                password_hash = generate_password_hash(password)
            )

            db.session.add(new_user)
            db.session.commit()
        
            flash(f"Successfully registered, {new_user.name}!", "primary")
            return redirect(url_for("auth.login"))

        flash(f"The user already exists!", "warning")
    # GET
    return render_template("user.html", heading="Register", form=register_form)

    # register_form = RegisterForm()
    # if register_form.validate_on_submit():
    #     # POST
    #     flash(f"Successfully registered, {register_form.user_name.data}!", "primary")
    #     return redirect(url_for("auth.login"))
    # # GET

    # return render_template("user.html", heading="Register", form=register_form)


    @bp.route('/login', methods=['GET', 'POST'])
def authenticate(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@bp.route('/logout', methods=["POST", "GET"])
def logout():
    flash(f"You have been logged out.", "info")
    return render_template("index.html")

