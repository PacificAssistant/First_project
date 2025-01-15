from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, BooleanField, FileField
from wtforms.validators import ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User, Posts
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NonEmptyString:
    def __call__(self, form, field):
        if not field.data or field.data.strip() == '':
            raise ValidationError('Field cannot be empty or whitespace')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    photo = FileField('photo', validators=[
        FileRequired(message='File is required!'),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Submit')

    def __init__(self, original_username=None, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class MakePosts(FlaskForm):
    post_body = TextAreaField('Post :)', validators=[Length(min=0, max=140), NonEmptyString()])
    submit = SubmitField('Submit')

    def __init__(self, post=None, *args, **kwargs):
        super(MakePosts, self).__init__(*args, **kwargs)
        self.post = post

    def post_is_not_none(self, username):
        if username.data != self.post:
            post = Posts.query.filter_by(body=self.post_body.data).first()
            if post is not None:
                raise ValidationError('Post cant be none')


class ChangeAvatar(FlaskForm):
    photo = FileField('Upload Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Submit')
