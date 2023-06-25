#!/usr/bin/env python3
"""Project Model"""
from datetime import datetime, timedelta
from .associations import user_projects, project_roles
from .base import BaseModel, db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum


class MeetingDay(BaseModel):
    __tablename__ = 'meeting_days'
    name = db.Column(db.String(64), unique=True, nullable=False)


meeting_days = db.Table('project_meeting_days',
                        db.Column('project_id', db.String(60), db.ForeignKey(
                            'projects.id'), primary_key=True),
                        db.Column('meeting_day_id', db.String(60), db.ForeignKey(
                            'meeting_days.id'), primary_key=True)
                        )


class Project(BaseModel):
    """
    Project Model
    Fields:
        name (str): Project name
        description (str): Project description
        status (str): Project status (Planning, Active, Complete, Unknown)
        deadline (datetime): Project deadline
        author_id (str): Project author's id

    Relationships:
        related_users (list): Users related to project
        author (User): Project author
    """
    __tablename__ = 'projects'
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    status = db.Column(
        Enum('Planning', 'Active', 'Complete', 'Unknown'), nullable=True)

    author_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    version = db.Column(db.String(64), nullable=True, default='0.0.0')

    start_date = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())
    deadline = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))

    # Relationships
    related_users = relationship(
        'User', secondary=user_projects, back_populates="related_projects")
    roles = relationship('Role', secondary=project_roles,
                         backref=db.backref('projects', lazy='dynamic'))
    author = relationship('User', backref='lead_projects')
    meeting_days = db.relationship(
        'MeetingDay', secondary=meeting_days, backref=db.backref('projects', lazy='dynamic'))

    def __repr__(self):
        return '<Project {}>'.format(self.name)
