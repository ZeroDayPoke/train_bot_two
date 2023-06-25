#!/usr/bin/env python3
"""Console module for the train_bot project"""

import cmd
from app import create_app, db
from app.models import Project
from app.models import User, Role

# Create Flask application from the factory
app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()

# Create a dictionary of classes
class_dictionary = {
    'Project': Project,
    'User': User,
    'Role': Role
}


class Bot_Console(cmd.Cmd):
    """Console class for the train_bot project"""
    prompt = '(tb_app) '
    last_output = ''

    def get_class(self, class_name):
        """Returns the class from the class dictionary"""
        return class_dictionary.get(class_name)

    def do_create(self, arg):
        """Creates a new instance of a class: create <class> <attribute1=value1> <attribute2=value2> ..."""
        with app.app_context():
            params = arg.split()
            if len(params) < 1:
                self.print(
                    "Usage: create <class> <attribute1=value1> <attribute2=value2> ...")
                return

            class_name = params.pop(0)
            cls = self.get_class(class_name)
            if cls is None:
                self.print(
                    f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            attributes = {}
            for param in params:
                key, value = param.split("=", 1)
                attributes[key] = value

        with app.app_context():
            if class_name == 'User' and 'role' in attributes:
                role_name = attributes.pop('role')
                password = attributes.pop('password', None)
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    self.print(f"Role {role_name} not found")
                    return
                instance = cls(**attributes)
                if password is not None:
                    instance.set_password(password)
                instance.roles.append(role)
            else:
                instance = cls(**attributes)

                db.session.add(instance)
                db.session.commit()
                self.print(f"{class_name} created with ID {instance.id}")

    def do_show(self, arg):
        """Show an instance of a class: show <class> <id>"""
        with app.app_context():
            params = arg.split()
            if len(params) < 2:
                self.print("Usage: show <class> <id>")
                return

            class_name, instance_id = params[0], params[1]
            cls = self.get_class(class_name)
            if cls is None:
                self.print(
                    f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instance = db.session.get(cls, instance_id)
            if instance is None and class_name == 'User':
                instance = cls.query.filter_by(username=instance_id).first()
            if instance is None:
                self.print(f"{class_name} with ID {instance_id} not found")
                print(f"{class_name} with ID {instance_id} not found")
            else:
                self.print(instance)
                print(instance)

    def do_destroy(self, arg):
        """Deletes an instance of a class: destroy <class> <id>"""
        with app.app_context():
            params = arg.split()
            if len(params) != 2:
                self.print("Usage: destroy <class> <id>")
                return

            class_name, instance_id = params
            cls = self.get_class(class_name)
            if cls is None:
                self.print(
                    f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instance = cls.query.get(instance_id)
            if instance is None:
                self.print(f"{class_name} with ID {instance_id} not found.")
                return

            db.session.delete(instance)
            db.session.commit()
            self.print(f"{class_name} with ID {instance_id} has been deleted.")

    def do_all(self, arg):
        """Displays all instances of a class: all <class>"""
        with app.app_context():
            params = arg.split()
            if len(params) != 1:
                self.print("Usage: all <class>")
                return

            class_name = params[0]
            cls = self.get_class(class_name)
            if cls is None:
                self.print(
                    f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instances = cls.query.all()
            for instance in instances:
                self.print(f"{class_name} {instance.id}: {instance}")

    def do_update(self, arg):
        """Updates an instance of a class: update <class> <id> <attribute1=value1> <attribute2=value2> ..."""
        with app.app_context():
            params = arg.split()
            if len(params) < 3:
                self.print(
                    "Usage: update <class> <id> <attribute1=value1> <attribute2=value2> ...")
                return

            class_name, instance_id = params[0], params[1]
            cls = self.get_class(class_name)
            if cls is None:
                self.print(
                    f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instance = cls.query.get(instance_id)
            if instance is None:
                self.print(f"{class_name} with ID {instance_id} not found")
                return

            attributes = {}
            for param in params[2:]:
                key, value = param.split("=", 1)
                attributes[key] = value

            if class_name == 'User' and 'role' in attributes:
                role_name = attributes.pop('role')
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    self.print(f"Role {role_name} not found")
                    return

                user = instance
                user.roles.append(role)
                db.session.commit()
                self.print(
                    f"Role {role_name} appended to User with ID {instance_id}")

            for key, value in attributes.items():
                setattr(instance, key, value)

            db.session.commit()
            self.print(f"{class_name} with ID {instance_id} has been updated.")

    def do_quit(self, arg):
        """Quit the console: quit"""
        self.print("Exiting console...")
        return True

    def print(self, msg):
        """Meows Bot Output Together"""
        if self.last_output:
            self.last_output += '\n' + msg
        else:
            self.last_output = msg

    def get_output(self):
        """Returns cat'd output"""
        return self.last_output

    def onecmd(self, line):
        """Override the onecmd method to print the output of the command"""
        self.last_output = ''
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)


    def do_hcf(self, arg):
        """Halts and catches fire: hcf"""
        with app.app_context():
            params = arg.split()
            if len(params) != 1:
                self.print("Usage: hcf <username>")
                return

            username = params[0]
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.print(f"User {username} not found")
                return

            if 'ADMIN' not in [role.name for role in user.roles]:
                self.print(f"User {username} is not an admin")
                return

            self.print("HCF")


    def user_exists(self, username):
        """Check if a user exists and return a boolean value."""
        self.onecmd(f"show User {username}")
        response = self.get_output()
        return "not found" not in response


if __name__ == "__main__":
    Bot_Console().cmdloop()
