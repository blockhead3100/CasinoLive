from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import random
import os
from flask_migrate import Migrate
import requests  # Python equivalent of axios

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
        bet = request.form.get('bet')  # Safely get the 'bet' value
        if not bet:
            return "Bet amount is required!", 400
        try:
            bet = float(bet)
        except ValueError:
            return "Invalid bet amount!", 400

        if bet < 1 or bet > user.balance:
            return "Bet must be between $1 and your current balance!", 400

        dice_roll = random.randint(1, 6)
        if dice_roll > 3:
            user.balance += bet
            result = f"You rolled a {dice_roll}. You win ${bet}!"
        else:
            user.balance -= bet
            result = f"You rolled a {dice_roll}. You lose ${bet}."
        db.session.commit()
        return render_template('dice.html', user=user, result=result)

    return render_template('dice.html', user=user)

@app.route('/slot-machine/<username>', methods=['GET', 'POST'])
def slot_machine(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return f"User {username} not found!", 404

    if request.method == 'POST':
        bet = request.form.get('bet')  # Safely get the 'bet' value
        if not bet:
            return "Bet amount is required!", 400
        try:
            bet = float(bet)
        except ValueError:
            return "Invalid bet amount!", 400

        if bet < 1 or bet > user.balance:
            return "Bet must be between $1 and your current balance!", 400

        symbols = ['🍒', '🍋', '🍊', '⭐', '💎']
        spin = [random.choice(symbols) for _ in range(3)]
        if spin[0] == spin[1] == spin[2]:
            user.balance += bet * 5  # Win 5x the bet amount
            result = f"Jackpot! You got {spin}. You win ${bet * 5}!"
        else:
            user.balance -= bet  # Lose the bet amount
            result = f"You got {spin}. You lose ${bet}."
        db.session.commit()
        return render_template('slot_machine.html', user=user, result=result)

    return render_template('slot_machine.html', user=user)

@app.route('/api/data', methods=['GET'])
def fetch_data():
    param = request.args.get('param', default='default_value')
    response = requests.get(f'https://api.example.com/data?param={param}')
    return jsonify(response.json())

# Add Poker and Blackjack routes
@app.route('/poker/<username>', methods=['GET', 'POST'])
def poker(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return f"User {username} not found!", 404

    if request.method == 'POST':
        # Poker logic placeholder
        return "Poker game logic goes here."

    return render_template('poker.html', user=user)

@app.route('/blackjack/<username>', methods=['GET', 'POST'])
def blackjack(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return f"User {username} not found!", 404

    if request.method == 'POST':
        # Retrieve game state from session
        deck = session.get('deck', [])
        player_hand = session.get('player_hand', [])
        dealer_hand = session.get('dealer_hand', [])

        # Handle player action
        action = request.form.get('action')
        if action == 'hit':
            player_hand.append(deck.pop())
            if sum(player_hand) > 21:  # Player busts
                return f"You busted! Dealer wins. Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
        elif action == 'stand':
            # Dealer's turn
            while sum(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            # Determine winner
            player_total = sum(player_hand)
            dealer_total = sum(dealer_hand)
            if dealer_total > 21 or player_total > dealer_total:
                return f"You win! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
            elif player_total < dealer_total:
                return f"Dealer wins! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
            else:
                return f"It's a tie! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"

        # Save updated game state
        session['deck'] = deck
        session['player_hand'] = player_hand
        session['dealer_hand'] = dealer_hand

        return render_template('blackjack_game.html', player_hand=player_hand, dealer_hand=[dealer_hand[0]])

    # Initialize a new game
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Save game state
    session['deck'] = deck
    session['player_hand'] = player_hand
    session['dealer_hand'] = dealer_hand

    return render_template('blackjack_game.html', player_hand=player_hand, dealer_hand=[dealer_hand[0]])

def some_function():
    pass  # Placeholder for future implementation

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()  # Create database tables only if they don't exist
    
    app.run(debug=True)

