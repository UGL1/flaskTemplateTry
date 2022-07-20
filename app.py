from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, url_for, flash, redirect,request,abort
from my_forms import *

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# app creation
app = Flask(__name__)

# login stuff
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'log_in' # nae of the login route function
login_manager.login_message = "Connexion requise pour accéder à la page."
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return UserDB.query.get(int(user_id))  # what is this ?


# forms
from my_ORM import *

# needed for forms & login
app.secret_key = "top cool"
db.create_all()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['get', 'post'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserDB.query.filter_by(user_name=form.user_name.data).first()
        if not user:
            flash(f"Le nom d'utilisateur {form.user_name.data} n'existe pas.", "danger")
            form.user_name.data = ""
        elif not user.password_match(form.password.data):
            flash("Mot de passe incorrect.", "danger")
        else:
            login_user(user,remember=form.remember.data)
            flash(f"Bienvenue {form.user_name.data} !", "success")
            #prevent open redirects
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route('/signup', methods=['get', 'post'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.password_match.data:
            flash(f"Les mots de passe ne correspondent pas.", "danger")
        else:
            user_same_username = UserDB.query.filter_by(user_name=form.user_name.data).first()
            if user_same_username:
                flash(f"Le nom d'utilisateur {form.user_name.data} est déjà pris.", "danger")
                form.user_name.data = ''
            else:
                user_same_email = UserDB.query.filter_by(email=form.email.data).first()
                if user_same_email:
                    flash(f"L'adresse {form.email.data} est déjà utilisée", "danger")
                    form.email.data = ''
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


@app.route('/logout')
@login_required
def log_out():
    name = current_user.user_name
    logout_user()
    flash(f"{name} est déconnecté.", "success")
    return redirect(url_for("index"))


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template("dashboard.html",user=current_user)


@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
