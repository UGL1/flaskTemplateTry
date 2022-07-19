from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired


# Here are all the forms used by the app
class SignUpForm(FlaskForm):
    first_name = StringField("Prénom", validators=[DataRequired()])
    last_name = StringField("Nom", validators=[DataRequired()])
    user_name = StringField("Nom d'utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    password_match = PasswordField("Confirmation du mot de passe", validators=[DataRequired()])
    submit = SubmitField("Valider")


class LoginForm(FlaskForm):
    user_name = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Valider")
