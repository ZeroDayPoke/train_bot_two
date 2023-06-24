#!/usr/bin/env python3
"""Admin routes."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

admin_routes = Blueprint('admin_routes', __name__)
