import os

from flask import Flask, jsonify
from flask_oauth2_login import GoogleLogin

from repository.models import *

app = Flask(__name__)

app.config.update(
  SECRET_KEY="secret",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

app.config.from_object('config.DevelopmentConfig')
google_login = GoogleLogin(app)
db.init_app(app)


@app.route('/')
def hello_world():
    create_database_if_needed(app)

    return """
    <html>
    Hello, please <a href="{}">Login with Google</a>
    """.format(google_login.authorization_url())


@google_login.login_success
def login_success(token, profile):

    return jsonify(token=token, profile=profile)



@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))
