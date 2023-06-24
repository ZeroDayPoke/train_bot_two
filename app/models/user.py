#!/usr/bin/env python3
"""User and Role Models"""

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .base import BaseModel, db
from sqlalchemy.orm import relationship
from .associations import user_roles, user_projects


class Role(BaseModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    discord_id = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    verification_token = db.Column(db.String(40), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    token_generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    roles = relationship('Role', secondary=user_roles,
                         backref=db.backref('users', lazy='dynamic'))
    related_projects = relationship(
        'Project', secondary=user_projects, back_populates="related_users")

    def __init__(self, *args, **kwargs):
        """creates new User"""
        password = kwargs.pop('password', None)
        super().__init__(*args, **kwargs)
        if password:
            self.set_password(password)

    def __repr__(self):
        """User representation"""
        return f'<User {self.username}>'

    def set_password(self, pwd):
        """encrypts password"""
        self.password_hash = generate_password_hash(pwd)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def token_expired(self):
        expiration_time = self.token_generated_at + timedelta(hours=24)
        return datetime.utcnow() > expiration_time
