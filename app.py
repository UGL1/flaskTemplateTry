from flask import Flask,flash, render_template, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'dummy'

@app.route('/')
def index():
    flash('Salut','success')
    flash('pas cool','error')
    flash('heho','info')
    return render_template("index.html")


@app.route('/login')
def log_in():
    pass


@app.route('/logout')
def log_out():
    pass


@app.route('/signup')
def sign_up():
    pass


@app.route('/dashboard')
def dashboard():
    pass


if __name__ == '__main__':
    app.run()
