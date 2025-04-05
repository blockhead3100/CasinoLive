from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Block/Documents/GitHub/CasinoLive/CasinoLive/casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()  # Create the SQLAlchemy instance without passing the app
db.init_app(app)  # Initialize the app with the SQLAlchemy instance

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login route

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Add authentication logic here
        if username == "test" and password == "password":  # Example logic
            return jsonify({"message": f"Welcome, {username}!"})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Add registration logic here
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
    return render_template('games/games.html')  # Correct path to the games.html file

@app.route('/roll_dice')
def roll_dice():
    return render_template('games/roll_dice.html')  # Replace with your actual roll dice page

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():  # Ensure the app context is active
            db.create_all()  # Create database tables only if they don't exist
    print("Database initialized successfully!")

    app.run(debug=True)