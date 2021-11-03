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
    error=None
    if (login_form.validate_on_submit() == True):
            username = login_form.user_name.data
            password = login_form.password.data

            check_user = User.query.filter_by(name = username).first()
            if check_user is None:
                error='Incorrect user name'

            if check_user is not None:
                if check_password_hash(check_user.password_hash, password):
                    flash(f"Welcome, {check_user.name}!", "success")
                    login_user(check_user)
                    return redirect(url_for("main.index"))
            flash(f"Incorrect credentials!", "warning")
    return render_template("user.html", heading="Login", form=login_form)
    

@bp.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if (register_form.validate_on_submit() == True):
            username = register_form.user_name.data
            contact_number = register_form.contact.data
            address = register_form.address.data
            email = register_form.email_id.data
            password = register_form.password.data

            check_user = User.query.filter_by(name=username).first()
            if check_user:
                flash('User already exists, please login')
                return redirect(url_for('auth.login'))
            if check_user is None:
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
    return render_template("user.html", heading="Register", form=register_form)


@bp.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash(f"You have been logged out.", "info")
    return redirect(url_for("main.index"))

