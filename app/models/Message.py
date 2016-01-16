""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
from flask import session
class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    def get_userpage_messages(self, wall_id):

        query="SELECT messages.message, messages.id, messages.created_at, messages.user_id, messages.wall_id, users.first_name, users.last_name FROM users LEFT JOIN messages ON users.id=messages.wall_id WHERE messages.user_id = {}".format(wall_id)

        return self.db.query_db(query)

    def get_userpage_comments(self, wall_id):
        query = "SELECT comments.comment, comments.created_at, comments.message_id, users.first_name, users.last_name FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE comments.wall_id = {}".format(wall_id)

        return self.db.query_db(query)

    def post_message(self, message_info):
        query = "INSERT INTO messages (message, user_id, wall_id, created_at, updated_at) VALUES ('{}', {}, {}, NOW(), NOW())".format(message_info['message'], message_info['wall_id'], message_info['user_id'])
        self.db.query_db(query)

    def post_comment(self, comment_info):
        query = "INSERT INTO comments (comment, user_id, message_id, wall_id, created_at, updated_at) VALUES ('{}', {}, {}, {}, NOW(), NOW())".format(comment_info['comment'], session['user_id'], comment_info['message_id'], comment_info['wall_id'])
        self.db.query_db(query)

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
