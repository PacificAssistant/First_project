import base64
import os
import sqlite3
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from werkzeug.utils import secure_filename


from app.log import general_logger,error_logger,user_log,check
from app import app, db
from app.forms import LoginForm, RegistrationForm, ChangeAvatar
from app.models import User, Posts
from datetime import datetime, timezone
from app.forms import EditProfileForm, MakePosts
from app.delete import delete_post_from_db



@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form['post_id']
    success = delete_post_from_db(post_id)
    if success:
        flash("Post deleted successfully")
    else:
        flash("An error occurred while deleting the post.")
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():  # Main page
    posts = Posts.query.all()

    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        connection = sqlite3.connect('app.db')
        connection.close()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Executing an SQL query to get the object ID
    cursor.execute(f"SELECT id FROM user WHERE username = ?", (username,))
    result = cursor.fetchone()
    user_id =result[0]
    conn.close()
    posts = db.session.query(Posts).filter_by(User_id=user_id).all()

    if user and user.image:
        # We encode the image in Base64
        image_data = base64.b64encode(user.image).decode('utf-8')
    else:
        image_data = None
    return render_template('user.html', user=user, posts=posts, image_data=image_data,)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        image = form.photo.data.read()
        user = User.query.filter_by(username=current_user.username).first()
        user.username = form.username.data
        user.about_me = form.about_me.data
        user.image = image
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/modal')
def modal():
    return render_template('modal.html')


@app.route('/Make_post', methods=['GET', 'POST'])
def make_post():
    form = MakePosts()
    if form.validate_on_submit():

        post = Posts(User_id=current_user.id, text=form.post_body.data)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('Make_post.html', form=form)


@app.route('/test_photo', methods=['GET', 'POST'])
def upload_image():
    form = ChangeAvatar()
    if form.validate_on_submit():
        check(1, current_user)
        user_log.info(f'{current_user}' '123456')

        # Processing the uploaded file
        file = form.photo.data
        filename = secure_filename(file.filename)  # Secure filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash(f'Post created with photo: {filename}')
        return redirect(url_for('user', username=current_user.username))

    return render_template('test_photo.html', form=form)


@app.route('/user/<username>')
def friend_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404

    return f"Welcome to {user.username}'s profile!"