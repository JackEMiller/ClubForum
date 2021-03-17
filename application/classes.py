from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    user_name = db.Column(db.String(30), primary_key = True, nullable = False)
    password = db.Column(db.String(30), nullable= False)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    level = db.Column(db.String(30), nullable=False)
    affiliation = db.Column(db.String(30), nullable=False)


class Techniques(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    difficulty = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)


class ClassesTechnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer,  db.ForeignKey('classes.id'),nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'),nullable=False)


class ClassesMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    technique_id = db.Column(db.Integer, db.ForeignKey('techniques.id'), nullable=False)