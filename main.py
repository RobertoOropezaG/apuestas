import os

from flask import Flask
from flask_oauth2_login import GoogleLogin

app = Flask(__name__)

app.config.update(
  SECRET_KEY="secret",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

app.config.from_object('config.DevelopmentConfig')


google_login = GoogleLogin(app)

@app.route('/')
def hello_world():
    return """
    <html>
    Hello, please <a href="{}">Login with Google</a>
    """.format(google_login.authorization_url())


