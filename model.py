from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """Show user info"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, 
                             default=datetime.utcnow)

    def __repr__(self):

            return f"<User user_id={self.user_id} username={self.username}>"

class Photo(db.Model):
    """Show photo info"""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_user_id = db.Column(db.Integer, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, 
                              default=datetime.utcnow)
    name = db.Column(db.String, nullable=True)
    photo_url = db.Column(db.String, nullable=False)

    hashtags = db.relationship("Hashtag", secondary="photohashtags",
                                backref="photos")

    
    def __repr__(self):

            return f"""<Photo photo_id={self.photo_id} 
                       photo_user_id={self.photo_user_id}
                       photo_url={self.photo_url}>"""


class Comment(db.Model):
    """Show comment about photo by user"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String, nullable=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.photo_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    users = db.relationship("User",
                               backref=db.backref("comments",
                                                  order_by=comment_id))
    photos = db.relationship("Photo",
                               backref=db.backref("comments",
                                                  order_by=comment_id))

    def __repr__(self):

            return f"""<Comment comment_id={self.comment_id} 
                       photo_id={self.photo_id}
                       user_id={self.user_id} 
                       >"""

class Hashtag(db.Model):
    """Show Hashtag info about photo"""

    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hashtag = db.Column(db.String, nullable=True, unique=True)
    
    def __repr__(self):

            return f"""<Hashtag hashtag_id={self.hashtag_id} 
                       hashtag={self.hashtag}>"""

class Photohashtag(db.Model):
    """Association table between photo and hashtag"""

    __tablename__ = "photohashtags"

    photohashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_id = db.Column(db.Integer, 
                         db.ForeignKey('photos.photo_id'), nullable=False)
    hashtag_id = db.Column(db.Integer, 
                           db.ForeignKey('hashtags.hashtag_id'), nullable=False)

    hashtags = db.relationship("Hashtag",
                               backref=db.backref("photohashtags",
                                                  order_by=photohashtag_id))
    photos = db.relationship("Photo",
                               backref=db.backref("photohashtags",
                                                  order_by=photohashtag_id))

    def __repr__(self):

            return f"""<Photohashtag photohashtag_id={self.photohashtag_id} 
                       photo_id={self.photo_id}
                       hashtag_id = {self.hashtag_id}>"""


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///instapic'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")




