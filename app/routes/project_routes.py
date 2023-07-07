#!/usr/bin/env python3
"""Project Routes for the Flask application"""
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Project, User, Role
from app.forms import ProjectForm

project_routes = Blueprint('project_routes', __name__, url_prefix='/projects')


@project_routes.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    form.related_users.choices = [(u.id, u.username) for u in User.query.all()]
    form.roles.choices = [(r.id, r.name) for r in Role.query.all()]
    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            description=form.description.data,
            status=form.status.data,
            author_id=current_user.id,
            version=form.version.data,
            meeting_days=form.meeting_days.data,
            repo_link=form.repo_link.data
        )
        related_users = User.query.filter(
            User.id.in_(form.related_users.data)).all()
        roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
        new_project.related_users = related_users
        new_project.roles = roles
        new_project.related_users.append(current_user)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully.', 'success')
        return redirect(url_for('project_routes.view_project',
                                current_user=current_user,
                                project_id=new_project.id))
    return render_template('projects.html', form=form)


@project_routes.route('/<project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    return render_template('view_project.html', project=project, form=form,
                           current_user=current_user)


@project_routes.route('/')
@login_required
def all_projects():
    projects = Project.query.all()
    form = ProjectForm()
    return render_template('all_projects.html', projects=projects, form=form,
                           current_user=current_user)


@project_routes.route('/delete_project/<project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    if not current_user.has_role('ADMIN'):
        flash('You do not have permission to delete projects.')
        return redirect(url_for('project_routes.all_projects'))
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully.')
    else:
        flash('Project not found.')
    return redirect(url_for('project_routes.all_projects'))


@project_routes.route('/update_project/<project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get(project_id)
    if project is None:
        flash('Project not found.')
        return redirect(url_for('project_routes.all_projects'))

    form = ProjectForm(obj=project)
    form.related_users.choices = [(u.id, u.username) for u in User.query.all()]
    form.roles.choices = [(r.id, r.name) for r in Role.query.all()]

    if form.validate_on_submit():
        # Update the project with the new data from the form
        project.name = form.name.data
        project.description = form.description.data
        project.status = form.status.data
        project.version = form.version.data
        related_users = User.query.filter(
            User.id.in_(form.related_users.data)).all()
        roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
        project.related_users = related_users
        project.roles = roles
        project.meeting_days = form.meeting_days.data
        project.repo_link = form.repo_link.data
        db.session.commit()
        flash('Project updated successfully.')
        return redirect(url_for('project_routes.update_project', project_id=project.id,
                                current_user=current_user))

    return render_template('view_project.html', form=form, project=project,
                           current_user=current_user)


@project_routes.route('/<project_id>/join', methods=['POST'])
@login_required
def add_user_to_project(project_id):
    user = current_user
    project = Project.query.get(project_id)
    if project is None:
        flash('Project not found.')
        return redirect(url_for('project_routes.all_projects'))
    if user not in project.related_users:
        project.related_users.append(user)
        db.session.commit()
        flash('You have joined the project.')
    else:
        flash('You are already a member of this project.')
    return redirect(url_for('project_routes.view_project', project_id=project.id,
                            current_user=current_user))
