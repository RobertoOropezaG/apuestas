from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Identity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    users = relationship('User', back_populates='identity')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(100), unique=True, nullable=False)
    identity_id = db.Column(db.Integer, db.ForeignKey('identity.id'))
    identity = relationship('Identity', back_populates='users')
    token = db.Column(db.String(200))


def seed_data(app):
    print('Seeding database')
    identity = Identity(email = 'oropezaroberto@gmail.com')
    db.session.add(identity)
    db.session.commit()