""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    def get_user_messages_comments(self, user_id):

        query="SELECT messages.message, messages.id, messages.created_at, messages.user_id, messages.wall_id comments.comment, comments.created_at, comments.user_id as com_user_id, users.first_name, com_users.first_name as com_first_name FROM users LEFT JOIN messages ON user.id=messages.wall_id LEFT JOIN comments ON messages.id=comments.message_id LEFT JOIN users as com_users  ON comments.user_id=com_users.id WHERE messages.user_id = {}".format(user_id)

        return self.db.query_db(query)

    def post_message(self):
        query = "INSERT INTO messages (message, user_id, wall_id, created_at, updated_at) VALUES ('{}', {}, {})".format(request.form['message'], request.form['wall_id'], session['user_id'])
        self.db.query_db(query)

    def post_comment(self):
        query = "INSERT INTO comments (comment, user_id, message_id, created_at, updated_at) VALUES ('{}', {}, {}, NOW(), NOW())".format(request.form['comment'], session['user_id'], request.form['message_id'])
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
