from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Photo, Comment, Hashtag, Photohashtag, Userphoto
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
@app.route('/photos', methods=['GET'])
def homepage():
    """Show a list of photos as homepage"""

    if not 'user_id' in session:

        return redirect('/login')

    photos = Photo.query.order_by(desc('date_uploaded')).all()

    return render_template('photo_list.html', photos=photos)


@app.route('/photos/<int:photo_id>/like.json', methods=['POST'])
def photo_like(photo_id):
    """Show num of likes for a photo"""

    photo_obj = Photo.query.filter_by(photo_id=photo_id).one()

    photo_obj.num_like = photo_obj.num_like + 1 if photo_obj.num_like else 1   

    db.session.commit()

    return jsonify(photo_obj.to_dict())
   

@app.route('/photos/<int:photo_id>/dislike.json', methods=['POST'])
def photo_dislike(photo_id):
    """Show num of dislikes for a photo"""

    photo_obj = Photo.query.filter_by(photo_id=photo_id).one()

    photo_obj.num_dislike = photo_obj.num_dislike + 1 if photo_obj.num_dislike else 1   

    db.session.commit()

    return jsonify(photo_obj.to_dict())


@app.route('/photos/<int:photo_id>/save.json', methods=['POST'])
def save_photo(photo_id):

    user_id = session['user_id']

    db_userphoto = Photo.query.options(db.joinedload('userphotos')).get(photo_id)

    new_userphoto = Userphoto(user_id=user_id, photo_id=photo_id)

    # userphoto object which includes all photos belong to same user
    db_userphoto.userphotos.append(new_userphoto)

    db.session.add(new_userphoto)
    db.session.commit()

    result = []

    for photo in db_userphoto.userphotos:

        result.append(photo.to_dict())

    return jsonify(result)


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


@app.route('/hashtag.json')
def hashtag_info():

    hashtags = Hashtag.query.all()

    list_hashtag = [hashtag.to_dict() for hashtag in hashtags]

    return jsonify(list_hashtag)


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
    
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    if 'user_id' in session:

        user_id = session['user_id']

        return redirect(f"/users/{user_id}")

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login form and stored in session"""

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).one()

    session['user_id'] = user.user_id

    if password != user.password:
        flash('Invalid password, please try again!')
        return redirect('login')

    flash(f"Welcome to Instapic, {user.username}")

    users = User.query.filter_by(username=username).one()

    return redirect(f"/users/{users.user_id}")

@app.route('/logout')
def logout():
    """delete session and let user logout"""

    del session['user_id']
    flash('You are logged out!')
    return redirect('/photos')


@app.route('/users/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    """User profile page that contains user information"""

    photos = Photo.query.order_by(desc('date_uploaded')).filter_by(photo_user_id=user_id).all()

    userphoto_lst = Userphoto.query.filter_by(user_id=user_id).order_by(desc('userphoto_id')).all()

    return render_template('user_profile.html', photos=photos, 
                            userphoto_lst=userphoto_lst)


@app.route('/photos/<int:photo_id>', methods=['GET'])
def photo_detail(photo_id):
    """Show individual photo information"""

    photo = Photo.query.get(photo_id)

    comment = Comment.query.filter_by(photo_id=photo_id)

    comment_lst = comment.order_by(desc('comment_id')).all()

    return render_template('photo_detail.html', photo=photo,
                            comment_lst=comment_lst)


@app.route('/photos/<int:hashtag_id>/hashtag', methods=['GET'])
def show_hashtag(hashtag_id):
    """Show list of photos when user click on hashtag for each photo"""

    photohashtags = Photohashtag.query.filter_by(hashtag_id=hashtag_id).all()

    return render_template('display_hashtag.html', photohashtags=photohashtags)


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

        return jsonify(result)


@app.route('/upload', methods=['GET'])
def upload_form():
    """Show upload form information"""

    if not session:

        return redirect('/')

    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Allow user to upload photos"""

    file = request.files['file']
    caption = request.form['caption']
    hashtag = request.form['hashtag']

    user_id = session['user_id']

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

        # return redirect(url_for('uploaded_file', filename=filename))
        return redirect(f'/users/{user_id}')

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



