class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    wins = db.Column(db.Integer, nullable=False, default=0)  # Track wins
    losses = db.Column(db.Integer, nullable=False, default=0)  # Track losses

<form method="POST">
    <label for="bet">Bet Amount:</label>
    <input type="number" id="bet" name="bet" min="1" required>
    <button type="submit">Roll the Dice</button>
</form>

if not bet:
    return "Bet amount is required!", 400
try:
    bet = float(bet)
except ValueError:
    return "Invalid bet amount!", 400