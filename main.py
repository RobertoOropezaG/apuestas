from flask import Flask, jsonify, redirect, url_for, render_template, make_response, request
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
def main():
    server_data = {'can_be_admin':current_user.can_be_admin,
                   'logged_as_admin':current_user.logged_as_admin}
    if not current_user.is_authenticated:
        return render_template('ask_login.html', login_url=google_login.authorization_url(),
                               server_data=server_data)
    else:
        return render_template('main.html', current_user=current_user,
                                server_data=server_data)


@google_login.login_success
def login_success(token, profile):
    user = authentication.save_login(token, profile)

    if not user:
        return jsonify(response='You can''t use this system with this email. Ask Roberto about this.',
                       email=profile['email'])

    login_user(user)

    return redirect(url_for('main')) #jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))


@app.route('/logout')
def logout():
    logout_user()
    return render_template('logged_out.html', login_url=google_login.authorization_url())


@login_manager.user_loader
def load_user(signature):
    user = authentication.get_user_by_signature(signature)
    return user


@app.route('/api/load_teams')
@login_required
def load_teams():
    result, error = matches.load_teams()

    if error: return make_response(jsonify(error=error), 201)

    return jsonify(response='success')


@app.route('/api/matches/<date>', methods=['GET'])
@login_required
def get_matches(date):
    matches.get_matches
    return jsonify(matches='not implemented')


@app.route('/api/admin/login', methods=['POST'])
@login_required
def admin_login():
    password = request.json['admin_password']
    user, error = authentication.authenticate_admin_password(password)
    
    if error:
        return make_response(jsonify(error=error), 401)

    login_user(user)

    return jsonify(message='logged in')


@app.route('/api/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    user, error = authentication.logout_admin()

    if error:
        return make_response(jsonify(error=error), 500)

    login_user(user)

    return jsonify(message='logged out')


if __name__ == '__main__':
    manager.run()