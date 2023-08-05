#!/usr/bin/env python3
"""Forms for the Flask application"""
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email
from wtforms.fields import SelectMultipleField
from wtforms_alchemy import ModelForm as WTFormsAlchemyModelForm, QuerySelectMultipleField
from app.models import User, Project, Role, MeetingDay
from flask_wtf.file import FileField, FileAllowed

from app.utils.upload_sets import photos

class ProfileUpdateForm(FlaskForm):
    user_image = FileField('Upload Profile Image', validators=[FileAllowed(photos, 'Images only!')])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ModelForm(WTFormsAlchemyModelForm, FlaskForm):
    pass


class ProjectForm(ModelForm):
    class Meta:
        model = Project

    related_users = SelectMultipleField(
        'Related Users', choices=[], coerce=str)
    roles = SelectMultipleField('Roles', choices=[], coerce=str)
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[('Planning', 'Planning'), (
        'Active', 'Active'), ('Complete', 'Complete'), ('Unknown', 'Unknown')])
    meeting_days = QuerySelectMultipleField('Meeting Days', query_factory=lambda: MeetingDay.query, get_label='name')
    repo_link = StringField('Repository Link')
    version = StringField('Version')
    deadline = StringField('Deadline')
