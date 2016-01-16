"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Messages(Controller):
    def __init__(self, action):
        super(Messages, self).__init__(action)
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

    def test(self):
        print "hello this is a test"
        return self.load_view('users/new.html')

    def show(self):
        return "this is the users show method"

    def create_msg(self):
        print '*' * 50
        print session['user_id']
        message_info = {
        'message': request.form['message'],
        'user_id': session['user_id'],
        'wall_id': request.form['wall_id']
        }
        self.models['Message'].post_message(message_info)
        return redirect('/users/show/'+str(request.form['wall_id']))