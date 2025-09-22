import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vybeflow.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    theme = db.Column(db.String(50), nullable=True, default='default')  # Add this line

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

class PostForm(FlaskForm):
    content = TextAreaField('What\'s on your mind?', validators=[DataRequired()])
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    phone = StringField('Phone Number', validators=[Length(min=0, max=20)])  # Added phone field
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ProfileForm(FlaskForm):
    theme = SelectField('Background Theme', choices=[
        ('default', 'Default'),
        ('dark', 'Dark'),
        ('blue', 'Blue'),
        ('nature', 'Nature')
    ])
    submit = SubmitField('Save Theme')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('signup'))
        user = User(username=form.username.data, phone=form.phone.data)  # Save phone
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('feed'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(content=form.content.data)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('feed'))
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('feed.html', form=form, posts=posts)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(theme=current_user.theme)
    if form.validate_on_submit():
        current_user.theme = form.theme.data
        db.session.commit()
        flash('Theme updated!')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form, theme=current_user.theme, user=current_user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <title>{{ user.username }}'s Profile</title>
    <style>
        body.default { background: #f0f0f0; }
        body.dark { background: #222; color: #fff; }
        body.blue { background: linear-gradient(to right, #2193b0, #6dd5ed); color: #fff; }
        body.nature { background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed; background-size: cover; color: #fff; }
        .profile-box { background: rgba(255,255,255,0.8); padding: 2em; margin: 2em auto; max-width: 400px; border-radius: 10px; }
    </style>
</head>
<body class="{{ theme }}">
    <div class="profile-box">
        <h2>{{ user.username }}'s Profile</h2>
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.theme.label }} {{ form.theme() }}<br><br>
            {{ form.submit() }}
        </form>
        <a href="{{ url_for('feed') }}">Back to Feed</a>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    </div>
</body>
</html>
