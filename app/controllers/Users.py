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
        print user_info
        if user_info['status'] == True:
            return redirect('/users/show/'+str(session['user_id']))
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
        user = self.models['User'].get_login_check(user_info)
        
        if user['status'] == True:
            id = session['user_id']
            return redirect('/users/show/'+str(id))
        else:
            flash('Email or password incorrect.')
            return redirect('/')


    def update(self): # Make sure to pass the ID from the URL
        format_user = {
        "id" : request.form['id'],
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email']
        }
        user_info = self.models['User'].update_user(format_user)
        if user_info['status'] == True:
            return redirect('/users/show/'+str(request.form['id']))
        else:
            for message in user_info['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def change_password(self):
        if request.form['password'] == request.form['pw_check'] and len(request.form['password']) > 7:
            self.models['User'].update_password(request.form['password'], session['user_id'])
            flash('Your password was changed successfully!')
            return redirect('/users/edit')
        else:
            flash('Your passwords did not match')
            return redirect('/users/edit')

    def show(self, id):
        user_info = self.models['User'].get_user_info(id)
        messages = self.models['Message'].get_userpage_messages(id)
        comments = self.models['Message'].get_userpage_comments(id)
        print session
        return self.load_view('/users/userwall.html', user_info=user_info, messages=messages, comments=comments)

    def dashboard(self):
        users = self.models['User'].get_all_users()

        return self.load_view('/users/dashboard.html', users=users)

    def admin_add_user(self):
        if session['user_level'] > 5:
            return self.load_view('/users/adduser.html')
        else:
            return redirect('/')

    def edit_user(self):
        user = self.models['User'].get_user_info(session['user_id'])
        return self.load_view('/users/edituser.html', user=user)

    def admin_edit_user(self, id):
        if session['user_level'] > 5:
            user = self.models['User'].get_user_info(id)

            return self.load_view('/users/adminedituser.html', user=user)

    def admin_update_user(self):
        format_user = {
        "id" : request.form['id'],
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email']
        }
        user_info = self.models['User'].update_user(format_user)
        self.models['User'].set_user_level(request.form['user_level'], request.form['id'])
        if user_info['status'] == True:
            return redirect('/users/show/'+str(request.form['id']))
        else:
            for message in user_info['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def delete_check(self, id):
        user_info = self.models['User'].get_user_info(id)
        return self.load_view('/users/delete.html', user_info=user_info)

    def delete(self):
        self.models['User'].delete_user(request.form['id'])
        return redirect('/users/dashboard')

    def logout(self):
        session.clear()
        return redirect('/')