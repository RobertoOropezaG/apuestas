import os

from flask import Flask, jsonify
from flask_oauth2_login import GoogleLogin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pprint import pprint

from repository.models import *


# Setup application and database
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
google_login = GoogleLogin(app)
db.init_app(app)

# Setup migrations
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    return """
    <html>
    Hello, please <a href="{}">Login with Google</a>
    """.format(google_login.authorization_url())


@google_login.login_success
def login_success(token, profile):
    identity = Identity.query.filter_by(email=profile['email']).first()

    if not identity:
        return jsonify(response='You can''t use this system with this email. Ask Roberto about this.', email=profile['email'])

    identity.update(profile)

    if not identity.users:
        user = User(nick=identity.first_name, token=token['access_token'])
        identity.users.append(user)
    elif len(identity.users) == 1:
        identity.users[0].token = token['access_token']

    db.session.commit()

    return jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))


if __name__ == '__main__':
    manager.run()