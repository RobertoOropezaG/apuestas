from flask import Flask, jsonify, redirect, url_for
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from repository.models import *


# Setup application and database
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)

# Setup migrations
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Setup authentication and login
google_login = GoogleLogin(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    if not current_user.is_authenticated:
        return """
        <html>
        Hello, please <a href="{}">Login with Google</a> to use this app
        """.format(google_login.authorization_url())
    else:
        return redirect(url_for('main'))


@google_login.login_success
def login_success(token, profile):
    identity = Identity.query.filter_by(email=profile['email']).first()

    if not identity:
        return jsonify(response='You can''t use this system with this email. Ask Roberto about this.', email=profile['email'])

    identity.update(profile)

    if not identity.users:
        user = User(nick=identity.first_name, token=token['access_token'])
        identity.users.append(user)
    else:
        user = identity.users[0]
        user.token = token['access_token']

    db.session.commit()

    login_user(user)

    return jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))


@app.route('/logout')
def logout():
    logout_user()
    return jsonify(message='You''ve been logged out')


@login_manager.user_loader
def load_user(user_id):
    print('loading user', user_id)
    try:
        user = User.query.get(user_id)
        return user
    except:
        return None


@app.route('/main')
@login_required
def main():
    return """
        <html>
        Hi {}, you are in the app <a href="{}">Logout</a> anytime.
        """.format(current_user.nick, url_for('logout'))


if __name__ == '__main__':
    manager.run()