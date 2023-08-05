#!/usr/bin/env python3
"""User and Role Models"""

from datetime import datetime, timedelta
from flask_login import UserMixin
from .base import BaseModel, db
from sqlalchemy.orm import relationship
from .associations import user_roles, user_projects
from flask_bcrypt import Bcrypt


class Role(BaseModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role {}'.format(self.name)


bcrypt = Bcrypt()


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    discord_id = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    verification_token = db.Column(db.String(40), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    token_generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    github_username = db.Column(db.String(64), unique=True, index=True)
    image_path = db.Column(db.String(256), nullable=True, default="default_employee.jpg")
    bio = db.Column(db.String(256), nullable=True)

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
        return f'{self.username} - {self.id}'

    def set_password(self, pwd):
        """encrypts password"""
        self.password_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def token_expired(self):
        expiration_time = self.token_generated_at + timedelta(hours=24)
        return datetime.utcnow() > expiration_time
