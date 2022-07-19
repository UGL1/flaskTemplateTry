from flask import Flask, render_template, url_for, flash, redirect
from my_forms import *

app = Flask(__name__)

from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from my_ORM import *

# app creation


# needed for forms & login
app.secret_key = "top cool"
db.create_all()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def log_in():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/logout')
def log_out():
    flash("Vous êtes déconnecté", "success")
    return redirect(url_for("index"))


@app.route('/signup', methods=['get', 'post'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.password_match.data:
            flash(f"Les mots de passe ne correspondent pas.","danger")
        else:
            user_same_username = UserDB.query.filter_by(user_name=form.user_name.data).first()
            if user_same_username:
                flash(f"Le nom d'utilisateur {form.user_name.data} est déjà pris.", "danger")
                form.user_name.data = ''
            else:
                user_same_email = UserDB.query.filter_by(email=form.email.data).first()
                if user_same_email:
                    flash(f"L'adresse {form.email.data} est déjà utilisée", "danger")
                    form.email.data=''
                else:
                    flash(f"Bienvenue {form.user_name.data}, ton compte a été créé.", "success")
                    user = UserDB(first_name=form.first_name.data,
                                  last_name=form.last_name.data,
                                  user_name=form.user_name.data,
                                  email=form.email.data,
                                  password=form.password.data)
                    db.session.add(user)
                    db.session.commit()
                    form.first_name.data = ''
                    form.last_name.data = ''
                    form.user_name.data = ''
                    form.email.data = ''
                    form.password = ''
                    form.password_match = ''
                    return redirect(url_for("log_in"))

    return render_template("signup.html", form=form)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
