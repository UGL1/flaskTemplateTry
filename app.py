from flask import Flask, render_template, url_for, flash, redirect

app = Flask(__name__)

from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from my_ORM import *

# app creation


# needed for forms & login
app.secret_key = "top cool"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def log_in():
    return render_template("login.html")


@app.route('/logout')
def log_out():
    return render_template("logout.html")


@app.route('/signup')
def sign_up():
    return render_template("signup.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
