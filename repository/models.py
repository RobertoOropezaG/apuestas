from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()


class Identity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    users = relationship('User', back_populates='identity')

    def update_from_google(self, profile):
        self.full_name = profile['name']
        self.first_name = profile['given_name']
        self.last_name = profile['family_name']
        self.picture = profile['picture']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(100), unique=True, nullable=False)
    identity_id = db.Column(db.Integer, db.ForeignKey('identity.id'))
    identity = relationship('Identity', back_populates='users')
    token = db.Column(db.String(200))


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code3 = db.Column(db.String(3), unique=True, nullable=False)
    code_fifa = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    flag_picture = db.Column(db.String(200))
    population = db.Column(db.Integer)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team1 = relationship('Team', uselist=False, foreign_keys=[team1_id])
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2 = relationship('Team', uselist=False, foreign_keys=[team2_id])
    finished = db.Column(db.Boolean)
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)


class Bettable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opened_since = db.Column(db.DateTime)
    closed_from = db.Column(db.DateTime)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    match = relationship('Match', uselist=False)


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bettable_id = db.Column(db.Integer, db.ForeignKey('bettable.id'))
    bettable = relationship('Bettable', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', uselist=False)
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)
    submitted_on = db.Column(db.DateTime, nullable=False)


def seed_data(app):
    print('Seeding database')
    identity = Identity(email='oropezaroberto@gmail.com')
    db.session.add(identity)
    db.session.commit()