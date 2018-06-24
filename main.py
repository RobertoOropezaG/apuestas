from flask import Flask, jsonify, redirect, url_for, render_template, make_response
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from repository.models import db
from logic import authentication, matches

# Setup application and database
app = Flask(__name__, static_folder='static')
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
        return render_template('ask_login.html', login_url=google_login.authorization_url())
    else:
        return render_template('main.html', current_user=current_user)


@google_login.login_success
def login_success(token, profile):
    user = authentication.save_login(token, profile)

    if not user:
        return jsonify(response='You can''t use this system with this email. Ask Roberto about this.',
                       email=profile['email'])

    login_user(user)

    return jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))


@app.route('/logout')
def logout():
    logout_user()
    return render_template('logged_out.html', login_url=google_login.authorization_url())


@login_manager.user_loader
def load_user(user_id):
    print('loading user', user_id)

    try:
        user = authentication.get_user_by_id(user_id)
        return user
    except:
        return None


@app.route('/api/load_teams')
@login_required
def load_teams():
    result, error = matches.load_teams()

    if error: return make_response(jsonify(error=error), 201)

    return jsonify(response='success')


if __name__ == '__main__':
    manager.run()