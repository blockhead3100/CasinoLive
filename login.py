from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casino.db'
db.init_app(app)

with app.app_context():
    print(app.jinja_env.list_templates())

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the game!"

if __name__ == "__main__":
    app.run(debug=True)