from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Credential(db.Model):
    __tablename__: "usuarios"
    #id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)


class Books(db.Model):
    __tablename__: "libros"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review_count = db.Column(db.Integer, nullable=False)
    average_score = db.Column(db.Float, nullable=False)

class Reviews(db.Model):
    __tablename__: "resenas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=True)
    review = db.Column(db.Integer, nullable=False)
    usuario = db.Column(db.String, nullable=False)
    rvwtext = db.Column(db.String, nullable=False)
    
