from flask import Flask, jsonify, redirect, url_for, render_template
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from repository.models import db
from logic import authentication

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
        return redirect(url_for('main'))


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
    return render_template('logged_out.html')


@login_manager.user_loader
def load_user(user_id):
    print('loading user', user_id)

    try:
        user = authentication.get_user_by_id(user_id)
        return user
    except:
        return None


@app.route('/main')
@login_required
def main():
    return render_template('main.html', nick=current_user.nick )


if __name__ == '__main__':
    manager.run()