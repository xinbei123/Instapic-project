from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Photo, Comment, Hashtag, Photohashtag
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import os

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "ABCdefGHL1234***$$$"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.jinja_env.undefined = StrictUndefined

# *******************************************************************************
# Functions Definitions

def allowed_file(filename):
    """parse the upload file"""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    """Show information about homepage"""

    return render_template('homepage.html')


@app.route('/photos', methods=['GET'])
def photo_list():
    """Show a list of photos"""

    photos = Photo.query.order_by(Photo.photo_id).all()

    return render_template('photo_list.html', photos=photos)


@app.route('/photos/like', methods=['POST'])
def photo_like():
    """Show likes of a photo"""

    photos = Photo.query.all()

    for photo in photos:
        photo.num_like = photo.num_like + 1 if photo.num_like else 1    

    db.session.commit()

    return render_template('photo_list.html', photos=photos)


@app.route('/photos/dislike', methods=['POST'])
def photo_dislike():
    """Show dislikes of a photo"""

    photos = Photo.query.all()

    for photo in photos:
        photo.num_like = photo.num_like - 1 if photo.num_like else 1    

    db.session.commit()

    return render_template('photo_list.html', photos=photos)


@app.route('/hashtag', methods=['GET'])
def hashtag_search():
    """Show hashtag search box"""

    return render_template('photo_hashtag.html')


@app.route('/hashtag', methods=['POST'])
def search_hashtag():
    """Show photo based on hashtag"""

    hashtag = request.form['hashtag']
    db_hashtag = Hashtag.query.filter_by(hashtag=hashtag).first()

    if not db_hashtag:

        flash('There is no matching photos!')
        return redirect('/hashtag')

    else:

        hashtag_id = Hashtag.query.filter_by(hashtag=hashtag).first().hashtag_id
        photohashtags = Photohashtag.query.filter_by(hashtag_id=hashtag_id).all()

        return render_template('hashtag.html', photohashtags=photohashtags)


@app.route('/register', methods=['GET'])
def register_form():
    """Show register form to user"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process register form and stored in db"""

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    new_user = User(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash('You are successfully registered!')
    
    return redirect('/photos')


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login form and stored in session"""

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    session['user_id'] = user.user_id
    flash('You are logged in!')

    return redirect('/photos')


@app.route('/logout')
def logout():
    """delete session and let user logout"""

    del session['user_id']
    flash('You are logged out!')
    return redirect('/photos')


@app.route('/photos/<int:photo_id>', methods=['GET'])
def photo_detail(photo_id):
    """Show individual photo information"""

    photo = Photo.query.get(photo_id)

    comment = Comment.query.filter_by(photo_id=photo_id)

    comment_lst = comment.order_by(desc('comment_id')).all()

    return render_template('photo_detail.html', photo=photo,
                            comment_lst=comment_lst)


# todo: make GET route for /photos/<int:photo_id>/comments

@app.route('/photos/<int:photo_id>/comments', methods=['POST'])
def make_comment(photo_id):
    """Allow user to make comments and stored in db"""

    comment = request.form.get('comment')
    user_id = session.get('user_id')

    if not session:
        flash('Please login to make comments!')
        return redirect('/login')

    else:

        db_photo = Photo.query.options(db.joinedload('comments')).get(photo_id)

        new_comment = Comment(comment=comment, user_id=user_id)

        db_photo.comments.append(new_comment)

        flash('comments added!')
        db.session.add(new_comment)
        db.session.commit()

        result = []

        for comment in db_photo.comments:

            result.append(comment.to_dict())

        # return redirect(f"/photos/{photo_id}")
        return jsonify(result)

@app.route('/upload', methods=['GET'])
def upload_form():
    """Show upload form information"""

    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Allow user to upload photos"""

    file = request.files['file']
    caption = request.form['caption']
    hashtag = request.form['hashtag']

    if not session:
        return redirect('/login')

    else:
        if file.name == '':
            flash('No selected photos')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            flash('Photo successfully uploaded')

            photo_user_id = session.get('user_id')

            new_photo = Photo(photo_user_id=photo_user_id, 
                              photo_url=('/' + file_path), caption=caption)

            db_hashtag = Hashtag.query.filter_by(hashtag=hashtag).first()

            if not db_hashtag:
                db_hashtag = Hashtag(hashtag=hashtag)

            new_photo.hashtags.append(db_hashtag)

            db.session.add(new_photo)
            db.session.commit()

            return redirect(url_for('uploaded_file', filename=filename))

        else:
            flash('Only png, jpg, jpeg, gif file types are allowed!')
            return redirect(request.url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(UPLOAD_FOLDER,filename)


#************************************************************************
# Helper Functions

if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



