from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# this do be garbage but I need a way for it to create a database in the current working directory
# and that's how sqlite expects it to look. Sue me (Like D:/ is not something it wants to hear right now, so we
# we gotta remove it, and then yeah.
temp = '/'.join(os.getcwd().replace("\\", '/').split('/')[1:])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////{temp}/new.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TEMP BULLSHIT AH1235412'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
HASHING_METHOD = 'pbkdf2:sha256'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    tasks_do = db.Column(db.String())
    tasks_done = db.Column(db.String())
    tasks_doing = db.Column(db.String())
    undo_data = db.Column(db.String())


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    if current_user.is_active:
        return redirect(f'/personal/{current_user.username}')
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if request.form.get('email').lower() not in [user.email for user in User.query.all()]:
            flash('Email not registered.')
        else:
            attempted_user = User.query.filter_by(email=request.form.get('email'))[0]
            if check_password_hash(pwhash=attempted_user.password_hash,
                                   password=request.form.get('password')):
                login_user(attempted_user)
                return redirect(f'../personal/{current_user.username}')
            else:
                flash('Incorrect password')
    return render_template('login_register.html', is_login=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Gotta be careful with this. Emails ain't case-sensitive.
        if request.form.get('email').lower() in [user.email for user in User.query.all()]:
            flash("Email already registered.")
        else:
            if request.form.get('password') != request.form.get('password-con'):
                flash("Passwords don't match.")
            else:
                new_user = User()
                # EMAILS AIN'T CASE SENSITIVE
                new_user.email = request.form.get('email').lower()
                new_user.password_hash = generate_password_hash(password=request.form.get('password'),
                                                                method=HASHING_METHOD,
                                                                salt_length=25)
                new_user.username = new_user.email.split('@')[0]
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_page'))
    return render_template('login_register.html', is_login=False)


@login_required
@app.route('/personal/<username>')
def user_page(username):
    # No idea why this has to be done. It's mad weird. I thought the login_required decorator would be enough.
    if not current_user.is_active:
        return redirect(url_for('homepage'))
    if current_user.username != username:
        return redirect(f'/personal/{current_user.username}')
    return render_template('index.html')


@login_required
@app.route('/personal/logout')
def logout():
    logout_user()
    return redirect('homepage')


if __name__ == '__main__':
    app.run(debug=True)
