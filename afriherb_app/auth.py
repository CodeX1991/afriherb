#!/usr/bin/python3
"""Create a Blueprint for routes"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exits.', category='error')
        elif password1 != password2:
            flash('Password did not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 1 character.', category='error')
        else:
            password_hash = generate_password_hash(password1)

            new_user = User(lastname=lastname, firstname=firstname, email=email,
                password=password_hash)
            
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully", category="success")
            return redirect(url_for('auth.login'))

    return render_template("signup.html")


@auth.route('/newsletter')
def newsletter():
    return render_template("newsletter.html")

@auth.route('/afriherb')
def afriherb():
    return render_template("home.html")