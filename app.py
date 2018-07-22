from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(

    SECRET_KEY='superuser',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:superuser@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False

)

db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def hello_flask():
    return 'Hello World!'


@app.route('/filters')
def filter_data():
    db.create_all()
    movies_dict = {'autopsy of jane doe': 2.14,
                    'neon demon': 3.20,
                    'ghost in a shell': 1.50,
                    'kong: skull island': 3.50,
                    'john wick 2': 2.52,
                    'spiderman - homecoming': 1.48 }

    return render_template('filter_data.html',
                           movies = movies_dict,
                           name = None,
                           film = 'a christmas carol')


class Publication(db.Model):

    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format( self.name)


class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, primary_key=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



