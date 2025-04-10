from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import logging

if not os.environ.get('SECRET_KEY'):
    logging.warning("SECRET_KEY is not set in the environment. Using fallback key.")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return {'user': user}
    return {'user': None}

@app.route('/')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!")
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user.is_admin:
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html', user=user)

@app.route('/admin/manage-users', methods=['GET', 'POST'])
def manage_users():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user.is_admin:
        flash("Access denied!")
        return redirect(url_for('home'))

    users = User.query.all()
    return render_template('admin/manage_users.html', user=user, users=users)

@app.route('/admin/dealer-tasks', methods=['GET', 'POST'])
def dealer_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user.is_admin:
        flash("Access denied!")
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        target_user_id = request.form.get('target_user_id')
        target_user = User.query.get(target_user_id)

        if action == 'distribute':
            points = float(request.form.get('points'))
            target_user.balance += points
            flash(f"Distributed {points} points to {target_user.username}.")
        elif action == 'collect':
            points = float(request.form.get('points'))
            target_user.balance -= points
            flash(f"Collected {points} points from {target_user.username}.")

        db.session.commit()
        return redirect(url_for('dealer_tasks'))

    return render_template('admin/dealer_tasks.html', user=user)

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)