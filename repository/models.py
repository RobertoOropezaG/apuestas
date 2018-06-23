from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Identity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    users = relationship('User', back_populates='identity')

    def update(self, profile):
        '''Update from google profile'''
        self.full_name = profile['name']
        self.first_name = profile['given_name']
        self.last_name = profile['family_name']
        self.picture = profile['picture']


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(100), unique=True, nullable=False)
    identity_id = db.Column(db.Integer, db.ForeignKey('identity.id'))
    identity = relationship('Identity', back_populates='users')
    token = db.Column(db.String(200))


def seed_data(app):
    print('Seeding database')
    identity = Identity(email='oropezaroberto@gmail.com')
    db.session.add(identity)
    db.session.commit()