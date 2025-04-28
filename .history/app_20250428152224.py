from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import logging
import openai
from sqlalchemy.orm import Session

# Add this after importing os
if not os.environ.get('SECRET_KEY'):
    logging.warning("SECRET_KEY is not set in the environment. Using fallback key.")

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# Ensure the database file exists in the correct location
if not os.path.exists('instance'):
    os.makedirs('instance')

if not os.path.exists('instance/casino.db'):
    open('instance/casino.db', 'w').close()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)  # Add this field
    wins = db.Column(db.Integer, default=0)  # Add wins column to the User model
    losses = db.Column(db.Integer, default=0)  # Add losses column to the User model

# Update user retrieval to use Session.get()
@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        with app.app_context():
            user = db.session.get(User, user_id)
        return {'user': user}
    return {'user': None}

@app.route('/')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    return render_template('index.html', user=user)

def hash_password(password):
    return generate_password_hash(password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash("Username and password are required!")
            return redirect(url_for('register'))
        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password)
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            app.logger.info(f"User {user.username} logged in successfully.")  # Log successful login
            return redirect(url_for('home'))  # Redirect to home page after login
        else:
            app.logger.warning("Invalid login attempt.")  # Log invalid login attempt
            flash("Invalid username or password!")
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/roll-dice', methods=['GET', 'POST'])
def roll_dice():
    user = User.query.first()  # Use the first user for now

    if request.method == 'POST':
        bet = request.form.get('bet')
        if not bet:
            flash("Bet amount is required!")
            return redirect(url_for('roll_dice'))
        try:
            bet = float(bet)
        except ValueError:
            flash("Invalid bet amount!")
            return redirect(url_for('roll_dice'))

        if bet < 1 or bet > user.balance:
            flash("Bet must be between $1 and your current balance!")
            return redirect(url_for('roll_dice'))

        dice_roll = random.randint(1, 6)
        if dice_roll > 3:
            user.balance += bet
            result = f"You rolled a {dice_roll}. You win ${bet}!"
        else:
            user.balance -= bet
            result = f"You rolled a {dice_roll}. You lose ${bet}."

        if user.balance < 0:
            user.balance = 0  # Reset balance to zero if it goes negative

        db.session.commit()
        return render_template('dice.html', user=user, result=result)

    return render_template('dice.html', user=user)

@app.route('/slot-machine', methods=['GET', 'POST'])
def slot_machine():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)

    if request.method == 'POST':
        symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
        reels = [random.choice(symbols) for _ in range(3)]

        if len(set(reels)) == 1:
            result = "Jackpot! You win $100!"
            user.balance += 100
        elif len(set(reels)) == 2:
            result = "Small win! You win $10!"
            user.balance += 10
        else:
            result = "You lose! Try again."
            user.balance -= 5

        if user.balance < 0:
            user.balance = 0  # Reset balance to zero if it goes negative
            db.session.commit()
        return render_template('slot_machine_result.html', reels=reels, result=result, user=user)

    return render_template('slot_machine.html', user=user)

@app.route('/poker', methods=['GET', 'POST'])
def poker():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)

    if request.method == 'POST':
        bet = request.form.get('bet')
        if not bet:
            flash("Bet amount is required!")
            return redirect(url_for('poker'))
        try:
            bet = float(bet)
        except ValueError:
            flash("Invalid bet amount!")
            return redirect(url_for('poker'))

        if bet < 1 or bet > user.balance:
            flash("Bet must be between $1 and your current balance!")
            return redirect(url_for('poker'))

        # Ensure deck is initialized
        deck = session.get('deck')
        if not deck:
            deck = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "♠♥♦♣"]
            random.shuffle(deck)
            session['deck'] = deck

        stage = session.get('stage', 0)
        community_cards = session.get('community_cards', [])
        player_hand = session.get('player_hand', [])

        if stage == 0:
            community_cards.extend([deck.pop() for _ in range(3)])
        elif stage == 1:
            community_cards.append(deck.pop())
        elif stage == 2:
            community_cards.append(deck.pop())
        else:
            winner = evaluate_poker_hand(player_hand, community_cards)
            if winner == "player":
                user.balance += bet
                result = f"You win ${bet}!"
            else:
                user.balance -= bet
                result = f"You lose ${bet}."
            if user.balance < 0:
                user.balance = 0  # Reset balance to zero if it goes negative
                db.session.commit()
            return render_template('poker_result.html', result=result, player_hand=player_hand, community_cards=community_cards)

        session['stage'] = stage + 1
        session['community_cards'] = community_cards
        session['deck'] = deck

        return render_template('poker_game.html', player_hand=player_hand, community_cards=community_cards, user=user)

    # Initialize a new game
    deck = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "♠♥♦♣"]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    community_cards = []

    session['deck'] = deck
    session['player_hand'] = player_hand
    session['community_cards'] = community_cards
    session['stage'] = 0

    return render_template('poker_game.html', player_hand=player_hand, community_cards=community_cards, user=user)

def evaluate_poker_hand(player_hand, community_cards):
    # Placeholder logic for poker hand evaluation
    all_cards = player_hand + community_cards
    ranks = [card[:-1] for card in all_cards]
    if len(set(ranks)) < len(ranks):  # Simple pair detection
        return "player"
    return "dealer"

@app.route('/blackjack', methods=['GET', 'POST'])
def blackjack():
    user = User.query.first()  # Use the first user for now

    if request.method == 'POST':
        bet = request.form.get('bet')
        if not bet:
            flash("Bet amount is required!")
            return redirect(url_for('blackjack'))
        try:
            bet = float(bet)
        except ValueError:
            flash("Invalid bet amount!")
            return redirect(url_for('blackjack'))

        if bet < 1 or bet > user.balance:
            flash("Bet must be between $1 and your current balance!")
            return redirect(url_for('blackjack'))

        # Initialize the game
        deck = session.get('deck')
        if not deck:
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
            random.shuffle(deck)
            session['deck'] = deck

        player_hand = session.get('player_hand', [deck.pop(), deck.pop()])
        dealer_hand = session.get('dealer_hand', [deck.pop(), deck.pop()])

        # Game logic
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)

        if player_total > 21:
            user.balance -= bet
            result = f"You busted! Dealer wins. Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
        elif dealer_total > 21 or player_total > dealer_total:
            user.balance += bet
            result = f"You win! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
        elif player_total < dealer_total:
            user.balance -= bet
            result = f"Dealer wins! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"
        else:
            result = f"It's a tie! Your hand: {player_hand}, Dealer's hand: {dealer_hand}"

        if user.balance < 0:
            user.balance = 0  # Reset balance to zero if it goes negative
            db.session.commit()
        return render_template('blackjack_game.html', user=user, result=result, player_hand=player_hand, dealer_hand=dealer_hand)

    # Render the game page with the bet form
    return render_template('blackjack_game.html', user=user)

@app.route('/games')
def games():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    return render_template('games/games.html', user=user)

@app.route('/admin')
def admin_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user.is_admin:
        flash("Access denied!")
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/dashboard.html', user=user, users=users)

@app.route('/admin/reset-balances', methods=['POST'])
def reset_balances():
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        flash("Access denied! Only admin can perform this action.")
        return redirect(url_for('admin_dashboard'))

    # Reset all user balances to zero
    users = User.query.all()
    for user in users:
        user.balance = 0.0
    db.session.commit()

    flash("All user balances have been reset to zero.")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-points', methods=['POST'])
def add_points():
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        flash("Access denied! Only admin can perform this action.")
        return redirect(url_for('admin_dashboard'))

    username = request.form.get('username')
    points = float(request.form.get('points', 0))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('admin_dashboard'))

    user.balance += points
    db.session.commit()

    flash(f"Added {points} points to {username}. New balance: {user.balance}")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/subtract-points', methods=['POST'])
def subtract_points():
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        flash("Access denied! Only admin can perform this action.")
        return redirect(url_for('admin_dashboard'))

    username = request.form.get('username')
    points = float(request.form.get('points', 0))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('admin_dashboard'))

    user.balance -= points
    if user.balance < 0:
        user.balance = 0  # Ensure no negative balance
    db.session.commit()

    flash(f"Subtracted {points} points from {username}. New balance: {user.balance}")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/set-points', methods=['POST'])
def set_points():
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        flash("Access denied! Only admin can perform this action.")
        return redirect(url_for('admin_dashboard'))

    username = request.form.get('username')
    points = float(request.form.get('points', 0))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('admin_dashboard'))

    user.balance = points
    db.session.commit()

    flash(f"Set {username}'s balance to {points} points.")
    return redirect(url_for('admin_dashboard'))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse the incoming JSON payload
        data = request.get_json()
        if not data:
            return {"error": "Invalid payload"}, 400

        # Log the received data (for debugging purposes)
        app.logger.info(f"Webhook received: {data}")

        # Process the data (customize this as needed)
        # Example: Respond to a specific event
        if data.get('event') == 'example_event':
            app.logger.info("Processing example_event")

        # Respond to the webhook
        return {"message": "Webhook received successfully"}, 200

    except Exception as e:
        app.logger.error(f"Error processing webhook: {e}")
        return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()
            # Ensure admin user exists
            admin_user = User.query.filter_by(username="admin").first()
            if not admin_user:
                admin_user = User(username="admin", password=hash_password("admin"), is_admin=True, balance=1000.0)
                db.session.add(admin_user)
                db.session.commit()
    app.run(debug=True)