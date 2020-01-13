from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creating DB instance
# db = SQLAlchemy(app)
db = SQLAlchemy(app, session_options={'autocommit': True})


# USER class
class User(db.Model):

    # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.String(100), nullable=False)
    # last_name = db.Column(db.String(100), nullable=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False, unique=True)
    # dob = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10),nullable=False)

    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()
        # db.session.close()

    def __repr__(self):
        return '<User %r>' % self.user_name

class LoggedUsers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(20), nullable=False)


    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()
        # db.session.close()

    def __repr__(self):
        return '<Users %r>' % self.user_id

class LoggedUsersPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
    time = db.Column(db.String(30), nullable=False)

    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()
        # db.session.close()

    def __repr__(self):
        return '<Post %r>' % self.user_id

class LoggedUsersComment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(2000), nullable=False)
    comment_time = db.Column(db.String(30), nullable=False)
    
    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()
        # db.session.close()

    def __repr__(self):
        return '<Comment %r>' % self.user_id