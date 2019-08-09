from flask import Flask, render_template, request, session
import requests


app = Flask(__name__)


CAT_PIC = {
    'auden': 'https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_960_720.jpg',
    'rocket': 'https://cdn.pixabay.com/photo/2017/07/25/01/22/cat-2536662_960_720.jpg',
    'muffin': 'https://cdn.pixabay.com/photo/2016/12/30/17/27/cat-1941089_960_720.jpg',
    'fido': 'https://cdn.pixabay.com/photo/2016/03/27/07/31/pet-1282309_960_720.jpg'
}


@app.route('/')
def homepage():

    return render_template('home.html', cats=CAT_PIC)

@app.route('/about')
def about():

    return render_template('about.html')












if __name__ == "__main__":
    app.run(debug=True)



