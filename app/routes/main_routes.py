#!/usr/bin/env python3
"""Main Routes for the Flask application"""
# app/routes/main_routes.py
from flask import render_template, Blueprint
from flask_login import current_user

main_routes = Blueprint('main_routes', __name__, url_prefix='')

@main_routes.route('/')
def index():
    return render_template('base.html', include_header=True, current_user=current_user)

@main_routes.route('/about')
def about():
    return render_template('about.html', include_header=True, current_user=current_user)

@main_routes.route('/business_plan')
def business_plan():
    return render_template('business_plan.html', include_header=True, current_user=current_user)
