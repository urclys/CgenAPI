# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo
from .models.users import User
from wtforms import ValidationError, validators
from app.base.tools import verify_pass


# login and registration


class SigninForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_login',
                             validators=[DataRequired()])

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(SigninForm, self).__init__(*k, **kk)

    def validate(self):
        self._user = User.query.filter_by(email=self.email.data).first()
        return super(SigninForm, self).validate()

    def validate_email(self, field):
        if self._user is None:
            raise ValidationError("Ce compte n'existe pas. Veuillez vérifier votre e-mail !")
        if not self._user.is_active:
            raise ValidationError("Votre compte n'est pas encore activé. Veuillez vérifier votre boite email !")

    def validate_password(self, field):
        if self._user is None:
            raise ValidationError()  # just to be sure
        if not verify_pass(field.data, self._user.password):  # passcheck embedded into user model
            raise ValidationError("Mot de passe incorrect. Veuillez vérifier votre mot de passe !")


# registration form for new users. not used in this project
# registration of new user is done by the admin users

# class SignupForm(FlaskForm):
#     class Meta:
#         csrf = False
#
#     email = StringField('Email', id='email_create',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Mot de passe',
#                              id='pwd_create',
#                              validators=[DataRequired(),
#                                          EqualTo('confirm_password'),
#                                          validators.Length(min=8,
#                                                            message='Mot de passe doit '
#                                                                    'contenir au moins 8 caractères !')])
#     confirm_password = PasswordField('Confirm Password')
#
#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first():
#             raise ValidationError('Cet email est déjà enregistré !')
#

class ForgotForm(FlaskForm):
    class Meta():
        csrf = False

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(ForgotForm, self).__init__(*k, **kk)

    def validate(self):
        self._user = User.query.filter_by(email=self.email.data).first()
        return super(ForgotForm, self).validate()

    def validate_email(self, field):
        if self._user is None:
            raise ValidationError("Ce compte n'existe pas. Veuillez vérifier votre e-mail !")


class ResetPasswordForm(FlaskForm):
    class Meta():
        csrf = False

    password = PasswordField('Mot de passe',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password'),
                                         validators.Length(min=8,
                                                           message='Mot de passe doit contenir au moins 8 caractère !')])
    confirm_password = PasswordField('Confirm Password')
