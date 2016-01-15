"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
from flask import session
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('index.html')
    def register(self):
        return self.load_view('/users/register.html')
    def create(self):
        format_user = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        "password" : request.form['password'],
        "pw_check" : request.form['pw_check']
        }
        user_info = self.models['User'].set_new_user(format_user)
        if user_info['status'] == True:
            return redirect('/users/success')
        else:
            for message in user_info['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def login(self):
        return self.load_view('/users/signin.html')
    def submitlogin(self):

        user_info = {
        'email': request.form['email'],
        'password' : request.form['password']
        }
        user = self.models['User'].validate_user(user_info)
        print user['status']
        if user['status'] == True:
            return redirect('/users/success')
        else:
            flash('Email or password incorrect.')
            return redirect('/')
    def edituser(self):
        self.load_view('/user/edituser.html')
    def update(self, id): # Make sure to pass the ID from the URL
        format_user = {
        "id" : id,
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email']
        }
        user_info = self.models['User'].update_user(format_user)
        if user_info['status'] == True:
            return redirect('/users/show/'+id)
        else:
            for message in user_info['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def show(self, id): # Padd ID from URL
        user_info = self.load_model('User').get_user_info(id)
        return self.load_view('/users/userwall.html', user_info=user_info)
