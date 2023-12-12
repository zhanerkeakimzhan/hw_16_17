from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

users = [
    {'id': str(uuid.uuid4()), 'username': 'jane', 'email': 'jane@gmail.com', 'bio': 'Introvert, kind'},
    {'id': str(uuid.uuid4()), 'username': 'aru', 'email': 'aru@aru.com', 'bio': 'Extravert, funny'},
]

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    bio = TextAreaField('Bio')

def get_user_by_id(user_id):
    return next((user for user in users if user['id'] == user_id), None)

@app.route('/')
def home():
    return redirect(url_for('get_profiles'))

@app.route('/profiles', methods=['GET'])
def get_profiles():
    return render_template('profiles.html', users=users)

@app.route('/profile/<string:user_id>', methods=['GET'])
def get_profile(user_id):
    user = get_user_by_id(user_id)
    
    if user:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('get_profiles'))

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm()

    if form.validate_on_submit():
        new_user = {
            'id': str(uuid.uuid4()),
            'username': form.username.data,
            'email': form.email.data,
            'bio': form.bio.data
        }
        users.append(new_user)
        return redirect(url_for('get_profiles'))

    return render_template('create_profile.html', form=form)

@app.route('/edit_profile/<string:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        # Находим пользователя в списке по user_id и обновляем его данные
        users[users.index(user)]['username'] = form.username.data
        users[users.index(user)]['email'] = form.email.data
        users[users.index(user)]['bio'] = form.bio.data

        # После обновления профиля перенаправляем на страницу с профилем
        return redirect(url_for('get_profile', user_id=user_id))

    return render_template('edit_profile.html', form=form, user=user)

@app.route('/delete_profile/<string:user_id>', methods=['GET', 'POST'])
def delete_profile(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return redirect(url_for('get_profiles'))

if __name__ == '__main__':
    app.run(debug=True)
