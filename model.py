from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

################################################################################
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

            return f"""<User user_id={self.user_id} username={self.username}"""


class Photo(db.Model):
    """Show photo info"""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_user_id = db.Column(db.Integer, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, 
                              default=datetime.utcnow)
    name = db.Column(db.String, nullable=True)
    photo_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)
    num_like = db.Column(db.Integer, nullable=True, default=0)
    num_dislike = db.Column(db.Integer, nullable=True, default=0)

    hashtags = db.relationship("Hashtag", secondary="photohashtags",
                                backref="photos")


    def __repr__(self):

        return f"""
        <Photo 
         photo_id={self.photo_id} 
         photo_user_id={self.photo_user_id}
         photo_url={self.photo_url}
         num_like={self.num_like}
         num_dislike={self.num_dislike}>
        """

    def to_dict(self):
        """Return a dictionary version of the photo likes and dislikes."""

        result = {}

        result['photo_id'] = self.photo_id
        result['num_like'] = self.num_like
        result['num_dislike'] = self.num_dislike

        return result


class Userphoto(db.Model):
    """Association table between users and photos"""

    __tablename__ = "userphotos"

    __table_args__ = (db.UniqueConstraint('user_id', 'photo_id'),)


    userphoto_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer, 
                         db.ForeignKey('users.user_id'), nullable=False)

    photo_id = db.Column(db.Integer, 
                         db.ForeignKey('photos.photo_id'), nullable=False) 

    users = db.relationship("User",
                               backref=db.backref("userphotos",
                                                  order_by=userphoto_id))
    photos = db.relationship("Photo",
                               backref=db.backref("userphotos",
                                                  order_by=userphoto_id))

    def __repr__(self):

            return f"""<Userphoto userphoto_id={self.userphoto_id} 
                       user_id={self.user_id}
                       photo_id = {self.photo_id}>"""

    def to_dict(self):
        """Return a dictionary version of the userphotos."""

        result = {}

        result['user_id'] = self.user_id
        result['photo_id'] = self.photo_id
        result['photo_url'] = self.photos.photo_url

        return result


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

        return f"""
        <Comment 
         comment_id={self.comment_id} 
         comment={self.comment}
         photo_id={self.photo_id}
         user_id={self.user_id} 
         >"""

    def to_dict(self):
        """Return a dictionary version of the comments."""

        result = {}
        
        result['comment_id'] = self.comment_id
        result['comment'] = self.comment
        result['user_id'] = self.user_id
        result['photo_id'] = self.photos.photo_id

        return result


class Hashtag(db.Model):
    """Show Hashtag info about photo"""

    __tablename__ = "hashtags"


    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hashtag = db.Column(db.String, nullable=True, unique=True)
    
    def __repr__(self):

            return f"""<Hashtag hashtag_id={self.hashtag_id} 
                                hashtag={self.hashtag}>"""

    def to_dict(self):
        """Return a dictionary version of the hashtags."""

        return {"hashtag_id": self.hashtag_id,
                "hashtag": self.hashtag}


class Photohashtag(db.Model):
    """Association table between photo and hashtag"""

    __tablename__ = "photohashtags"

    __table_args__ = (db.UniqueConstraint('hashtag_id', 'photo_id'),)

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

    def to_dict(self):
        """Return a dictionary version of the photohashtags"""

        result = {}

        result['hashtag_id'] = self.hashtag_id
        result['photo_id'] = self.photo_id
        result['photo_url'] = self.photos.photo_url

        return result


def example_data():
    """Create some sample data"""

    # In case this is run more than once, empty out existing data
    User.query.delete()

    # Add sample hashtags
    maggie = User(username='mlion', email='mlion@gmail.com', password=111111)

    db.session.add(maggie)
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///instapic'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)
    print("Connected to DB.")




