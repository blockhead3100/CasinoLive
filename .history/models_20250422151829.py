from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Block/Documents/GitHub/CasinoLive/CasinoLive/casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

if not os.path.exists('casino.db'):
    with app.app_context():
        db.create_all()  # Place a breakpoint here
        print("Database initialized successfully!")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Block/Documents/GitHub/CasinoLive/CasinoLive/casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)  # New column for admin status

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "test" and password == "password":
            return jsonify({"message": f"Welcome, {username}!"})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return jsonify({"message": f"User {username} registered successfully!"})
    return render_template('auth/register.html')

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if request.method == 'POST':
        bet = request.form.get('bet')
        if not bet:
            return jsonify({"error": "Bet amount is required!"}), 400
        try:
            bet = float(bet)
        except ValueError:
            return jsonify({"error": "Invalid bet amount!"}), 400
        return jsonify({"message": f"Bet of {bet} accepted!"})
    return render_template('bet_form.html')

@app.route('/games')
def games():
    return render_template('games/games.html')

@app.route('/roll_dice')
def roll_dice():
    return render_template('games/roll_dice.html')

@app.route('/create_admin', methods=['POST'])
def create_admin():
    secret_key = request.form.get('secret_key')
    if secret_key != "your_secret_key":  # Replace with your actual secret key
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = password  # Replace with a hashing function like werkzeug.security.generate_password_hash
    admin_user = User(username=username, password=hashed_password, is_admin=True, balance=0.0)

    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()

    return jsonify({"message": f"Admin account '{username}' created successfully!"})

@app.route('/admin/add_points', methods=['POST'])
def add_points():
    admin_id = session.get('user_id')
    admin_user = User.query.get(admin_id)

    if not admin_user or not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form.get('username')
    points = float(request.form.get('points', 0))

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.balance += points
    db.session.commit()

    return jsonify({"message": f"Added {points} points to {username}. New balance: {user.balance}"})

@app.route('/admin/subtract_points', methods=['POST'])
def subtract_points():
    admin_id = session.get('user_id')
    admin_user = User.query.get(admin_id)

    if not admin_user or not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form.get('username')
    points = float(request.form.get('points', 0))

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.balance -= points
    db.session.commit()

    return jsonify({"message": f"Subtracted {points} points from {username}. New balance: {user.balance}"})

@app.route('/admin/clear_points', methods=['POST'])
def clear_points():
    admin_id = session.get('user_id')
    admin_user = User.query.get(admin_id)

    if not admin_user or not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.balance = 0.0
    db.session.commit()

    return jsonify({"message": f"Cleared points for {username}. New balance: {user.balance}"})

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()
        print("Database initialized successfully!")

    app.run(debug=True)