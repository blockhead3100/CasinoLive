# filepath: c:\Users\Block\CasinoLive\src\main.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to CasinoLive!"

@app.route('/games')
def games():
    return "Welcome to the Games Page!"

if __name__ == '__main__':
    app.run(debug=True)