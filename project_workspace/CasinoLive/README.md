# CasinoLive Project

## Overview
CasinoLive is a web-based casino application built with Flask. It allows users to play various casino games, manage their accounts, and provides an admin interface for managing users and dealer tasks.

## Features
- User registration and login
- Various casino games including Dice, Slot Machine, Poker, and Blackjack
- Admin dashboard for managing user accounts
- Dealer tasks for distributing and collecting points

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CasinoLive.git
   ```
2. Navigate to the project directory:
   ```
   cd CasinoLive
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   python app.py
   ```

## Usage
1. Start the application:
   ```
   python app.py
   ```
2. Open your web browser and go to `http://127.0.0.1:5000/`.

## Admin Access
- The application restricts access to a single admin account.
- Admins can manage user accounts and perform dealer tasks.

## Note
- The registration functionality has been disabled to prevent the creation of new accounts. Only the admin can manage user accounts.

## License
This project is licensed under the MIT License.