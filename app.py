from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

@app.route('/')
def home():
    users = User.query.all()  # Fetch all users from the database
    return render_template('index.html', users=users)

@app.route('/games')
def games():
    return "Welcome to the Games Page!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']
    return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    if username:
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            # Add the new user to the database
            new_user = User(username=username, balance=100.0)  # Default balance
            db.session.add(new_user)
            db.session.commit()
    return redirect(url_for('home'))

@app.route('/roll-dice/<username>', methods=['GET', 'POST'])
def roll_dice(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return f"User {username} not found!", 404

    if request.method == 'POST':
        dice_roll = random.randint(1, 6)
        if dice_roll > 3:
            user.balance += 10  # Win $10
            result = f"You rolled a {dice_roll}. You win $10!"
        else:
            user.balance -= 5  # Lose $5
            result = f"You rolled a {dice_roll}. You lose $5."
        db.session.commit()
        return render_template('dice.html', user=user, result=result)

    return render_template('dice.html', user=user)

@app.route('/slot-machine/<username>', methods=['GET', 'POST'])
def slot_machine(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return f"User {username} not found!", 404

    if request.method == 'POST':
        # Simulate slot machine spin
        symbols = ['🍒', '🍋', '🍊', '⭐', '💎']
        spin = [random.choice(symbols) for _ in range(3)]

        # Check if all symbols match
        if spin[0] == spin[1] == spin[2]:
            user.balance += 50  # Win $50
            result = f"Jackpot! You got {spin}. You win $50!"
        else:
            user.balance -= 10  # Lose $10
            result = f"You got {spin}. You lose $10."

        db.session.commit()
        return render_template('slot_machine.html', user=user, result=result)

    return render_template('slot_machine.html', user=user)

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()  # Create database tables only if they don't exist
    app.run(debug=True)