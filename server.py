from flask import Flask, render_template, request, redirect, session, flash

from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Photo, Comment, Hashtag, Photohashtag


app = Flask(__name__)
app.secret_key = "ABCdefGHL1234***$$$"

app.jinja_env.undefined = StrictUndefined


# CAT_PIC = {
#     'auden': 'https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_960_720.jpg',
#     'rocket': 'https://cdn.pixabay.com/photo/2017/07/25/01/22/cat-2536662_960_720.jpg',
#     'muffin': 'https://cdn.pixabay.com/photo/2016/12/30/17/27/cat-1941089_960_720.jpg',
#     'fido': 'https://cdn.pixabay.com/photo/2016/03/27/07/31/pet-1282309_960_720.jpg'
# }


@app.route('/')
def homepage():
    """Show information about homepage"""

    return render_template('homepage.html')


@app.route('/photos', methods=['GET'])
def photo_list():
    """Show a list of photos"""

    photos = Photo.query.all()
    return render_template('photo_list.html', photos=photos)


@app.route('/hashtag', methods=['GET'])
def hashtag_search():
    """Show hashtag search box"""

    return render_template('photo_hashtag.html')


@app.route('/hashtag', methods=['POST'])
def search_hashtag():
    """Show photo based on hashtag"""

    hashtag = request.form['hashtag']

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

    return render_template('photo_detail.html', photo=photo)


@app.route('/photos/<int:photo_id>', methods=['POST'])
def make_comment(photo_id):
    """Allow user to make comments and stored in db"""

    comment = request.form.get('comment')

    user_id = session.get('user_id')

    if not user_id:
        flash('Please login to make comments!')
        return redirect('/login')

    new_comment = Comment(comment=comment, photo_id=photo_id, 
                          user_id=user_id)

    flash('comments added!')
    db.session.add(new_comment)
    db.session.commit()

    return redirect(f"/photos/{photo_id}")


if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



