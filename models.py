class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    wins = db.Column(db.Integer, nullable=False, default=0)  # Track wins
    losses = db.Column(db.Integer, nullable=False, default=0)  # Track losses

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    if not os.path.exists('casino.db'):
        with app.app_context():
            db.create_all()  # Create database tables only if they don't exist

    app.run(debug=True)