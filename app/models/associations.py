#!/usr/bin/env python3
"""Associations"""
# Path: train_bot/app/models/associations.py
from .base import db

project_roles = db.Table(
    'project_roles',
    db.Column('project_id', db.String(60), db.ForeignKey('projects.id'), primary_key=True),
    db.Column('role_id', db.String(60), db.ForeignKey('roles.id'), primary_key=True)
)

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.String(60), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.String(60), db.ForeignKey('roles.id'), primary_key=True)
)

user_projects = db.Table(
    'user_projects',
    db.Column('user_id', db.String(60), db.ForeignKey('users.id'), primary_key=True),
    db.Column('project_id', db.String(60), db.ForeignKey('projects.id'), primary_key=True)
)
