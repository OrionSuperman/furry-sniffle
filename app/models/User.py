""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
from flask import session
from flask.ext.bcrypt import Bcrypt
class User(Model):
    def __init__(self):
        super(User, self).__init__()

    # Function to return a list of all users for display. Can be modified to accept a range of users for scalability in the future.
    def get_all_users(self):
        return self.db.query_db("SELECT * FROM users") 

    # Function to select a single user and return all information stored in the database about them
    def get_user_info(self, id):

        user = self.db.query_db("SELECT * FROM users WHERE id={}".format(id))
        return user[0]

    def update_password(self, password, id):
        pass_hash = self.bcrypt.generate_password_hash(password)
        query = "UPDATE users SET pass_hash='{}' WHERE id={}".format(pass_hash, id)

    # Function to check a new user's submitted information and if it passes checks, upload to the server.
    def set_new_user(self, user_info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not user_info['first_name']:
            errors.append('First name cannot be blank')
        elif len(user_info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')

        if not user_info['last_name']:
            errors.append('Last name cannot be blank')
        elif len(user_info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')

        if not user_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email format must be valid!')
        

        if not user_info['password']:
            errors.append('Password must not be blank')
        elif len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user_info['password'] != user_info['pw_check']:
            errors.append('Passwords must match!')

        if errors:
            return {'status':False, 'errors':errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(user_info['password'])
            query = "INSERT INTO users (first_name, last_name, email, pass_hash, user_level, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', 1, NOW(), NOW())".format(user_info['first_name'], user_info['last_name'], user_info['email'], pw_hash)
            self.db.query_db(query)
            id_query = "SELECT * FROM users WHERE email='{}' LIMIT 1".format(user_info['email'])
            user=self.db.query_db(id_query)

            # The very first user to sign up will be set to an administrator(level 9). Hard coding the query to prevent a glitch from setting different users to admin. 
            if user[0]['id'] == 1:
                self.db.query_db("UPDATE users SET user_level=9 WHERE id=1")
                user=self.db.query_db(id_query)
            print user
            session['user_id'] = user[0]['id']
            session['first_name'] = user[0]['first_name']
            session['user_level'] = user[0]['user_level']
            return {'status':True, 'user':user[0]}

    # Function to update an existing users's non-password information in the database. All the same checks need to occur for validation.
    def update_user(self, user_info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not user_info['first_name']:
            errors.append('First name cannot be blank')
        elif len(user_info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')

        if not user_info['last_name']:
            errors.append('Last name cannot be blank')
        elif len(user_info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')

        if not user_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email format must be valid!')

        if errors:
            return {'status':False, 'errors':errors}
        else:
            query = "UPDATE users SET first_name='{}', last_name='{}', email='{}' WHERE id={}".format(user_info['first_name'], user_info['last_name'], user_info['email'], user_info['id'])
            print query
            self.db.query_db(query)
            
            return {'status':True}

    # Function to compare the supplied email and password combination to those in the server.
    def get_login_check(self, info):
        query = "SELECT * FROM users WHERE email='{}'".format(info['email'])
        user = self.db.query_db(query)
        print '*' * 50
        print user
        pass_hash = user[0]['pass_hash']
        password = info['password']

        if self.bcrypt.check_password_hash(pass_hash, password):
            status = True
            session['user_id'] = user[0]['id']
            session['first_name'] = user[0]['first_name']
            session['user_level'] = user[0]['user_level']

            return {'status':True}
        else:
            return {'status':False}

    def set_user_level(self, user_level, id):
        query = "UPDATE users SET user_level={} WHERE id={}".format(user_level, id)
        self.db.query_db(query)

    def delete_user(self, id):
        self.db.query_db("DELETE FROM users WHERE id={}".format(id))

    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
