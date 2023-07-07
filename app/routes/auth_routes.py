#!/usr/bin/env python3
"""Auth Routes for the app"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, User, Role
from ..forms import SignupForm, SigninForm

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/auth')

@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        
        """role_name = form.role.data
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)
        else:
            flash('Invalid role selected. Please try again.')
            return render_template('signup.html', form=form)"""

        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main_routes.index'))
    return render_template('signup.html', form=form)


@auth_routes.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Successfully signed in.')
            return redirect(url_for('main_routes.index'))
        else:
            flash('Invalid email or password. Please try again.')
    return render_template('signin.html', form=form)


@auth_routes.route('/signout', methods=['GET'])
@login_required
def signout():
    """Sign out the current user and redirect to the home page"""
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('main_routes.index'))


@auth_routes.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html', current_user=current_user)


@auth_routes.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Verify that the current password is correct
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.')
        return redirect(url_for('auth_routes.account'))

    # Verify that the new password and confirmation match
    if new_password != confirm_password:
        flash('New password and confirmation do not match.')
        return redirect(url_for('auth_routes.account'))

    # Update the user's password
    current_user.set_password(new_password)
    db.session.commit()

    flash('Your password has been updated.')
    return redirect(url_for('auth_routes.account'))
