# Drink Up! Cocktail API Search

## Project Overview

Drink Up! is a web application built with Python, Flask, PostgreSQL, and SQLAlchemy that allows users to search for cocktail recipes and manage their favorite drinks. Users can register, log in, and save their favorite drinks to a personalized list. This project utilizes the CocktailDB API to fetch cocktail data.

Site deployed: [https://cocktailsapi3.onrender.com/](https://cocktailsapi3.onrender.com/)

### Features

* **User Authentication** : Users can register, log in, and log out using secure password hashing.
* **Search Cocktails** : Users can search for cocktails using the CocktailDB API and view details of selected cocktails.
* **Favorite Management** : Registered users can add cocktails to their favorites and view their favorite cocktails list.
* **Dynamic Content Rendering** : The application dynamically renders cocktail data and manages favorites using embedded JavaScript code.

![1716887999837](image/README/1716887999837.png)

![1716888509420](image/README/1716888509420.png)

![1716888673315](image/README/1716888673315.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Seeding Data](#seeding-data)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Features

- User registration and authentication

  ![1716888092937](image/README/1716888092937.png)

  ![1716888119152](image/README/1716888119152.png)
- Search for cocktails using the CocktailDB API

  ![1716888195502](image/README/1716888195502.png)
- View detailed information about each cocktail

  ![1716888287341](image/README/1716888287341.png)
- Add and remove cocktails from single drink page

  ![1716888434977](image/README/1716888434977.png)
- Responsive design for various device sizes

  ![1716889274858](image/README/1716889274858.png)

  ![1716889289108](image/README/1716889289108.png)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HaykeesComet/CocktailsAPI3.git
   cd CocktailsAPI3
   ```
2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following:

   ```bash
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

## Configuration

Update the `config.py` file if necessary. The configuration includes setting up the secret key and database URL:

```python
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/cocktail_database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Database Setup

1. **Create the database:**
   Ensure PostgreSQL is running and create a new database:

   ```sql
   CREATE DATABASE cocktail_database;
   ```
2. **Initialize the database:**
   Run the following commands to create the necessary tables:

   ```bash
   python run.py
   ```
3. **Seed the database:**
   Insert initial data into the database by running:

   ```bash
   python seed.py
   ```

## Seeding Data

The `seed.py` file contains the script to seed the database with initial data:

```python
from werkzeug.security import generate_password_hash
from models import db, User, Favorite
from app import app

def seed_data():
    with app.app_context():
        db.create_all()

        user1 = User(username='john_doe', password=generate_password_hash('password123', method='pbkdf2:sha256'))
        user2 = User(username='jane_doe', password=generate_password_hash('password123', method='pbkdf2:sha256'))

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        favorite1 = Favorite(user_id=user1.id, drink_id='11007', drink_name='Margarita', drink_image='https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg')
        favorite2 = Favorite(user_id=user2.id, drink_id='11000', drink_name='Mojito', drink_image='https://www.thecocktaildb.com/images/media/drink/metwgh1606770327.jpg')

        db.session.add(favorite1)
        db.session.add(favorite2)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
```

## Running the Application

To run the application locally, execute:

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

## Project Structure

```
DrinkUp/
│
├── app.py                # Application setup and initialization
├── cocktail_seed.sql     # SQL file for creating initial database schema
├── config.py             # Configuration file
├── forms.py              # Flask-WTF form classes
├── models.py             # SQLAlchemy models and database setup
├── requirements.txt      # Project dependencies
├── run.py                # Script to run the application
├── seed.py               # Script to seed the database
├── views/
│   ├── __init__.py       # Blueprint initialization
│   ├── auth.py           # Authentication routes and views
│   └── drinks.py         # Drink-related routes and views
├── templates/
│   ├── layout.html       # Base HTML layout
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── index.html        # Main search and results page
│   ├── drink.html        # Single drink details page
│   └── favorites.html    # User's favorite drinks page
└── static/
    └── styles.css        # CSS styles
```

### Files Description

1. **app.py**
   * Initializes the Flask application, configures the database, and registers blueprints for authentication and drinks.
2. **config.py**
   * Contains the configuration for the Flask application, including secret keys and database URI.
3. **models.py**
   * Defines the database models for User and Favorite using SQLAlchemy.
4. **forms.py**
   * Defines WTForms for user login and registration.
5. **views/auth.py**
   * Handles routes for user authentication including login, registration, and logout.
6. **views/drinks.py**
   * Manages routes for searching cocktails, viewing details, and managing favorites.
7. **templates/**
   * Contains HTML templates for rendering the web pages.
8. **static/styles.css**
   * CSS file for styling the application.
9. **seed.py**
   * Seeds the database with initial data.
10. **run.py**
    * Script to run the Flask application.
11. **cocktail_seed.sql**
    * SQL script for creating the database schema.
12. **requirements.txt**
    * Lists the Python dependencies required for the project.

### Key Functionality

* **User Authentication**
  * `auth_bp`: Blueprint for authentication routes.
  * `LoginForm`, `RegisterForm`: WTForms for login and registration.
  * User model with secure password hashing using `werkzeug.security`.
* **Cocktail Search and Details**
  * `drinks_bp`: Blueprint for drink-related routes.
  * Integrates with the CocktailDB API to fetch cocktail data.
  * Dynamic rendering of cocktail details and ingredients.
* **Favorite Management**
  * Allows users to add and remove favorite cocktails.
  * Favorite cocktails are displayed on the user's favorites page.

### Usage

* **Register and Login**
  * Users can register with a username and password.
  * After logging in, users can search for cocktails and manage their favorites.
* **Searching Cocktails**
  * Use the search bar on the home page to find cocktails by name.
  * Click on a cocktail to view its details, including ingredients and instructions.
* **Managing Favorites**
  * Logged-in users can add cocktails to their favorites list.
  * Favorites can be accessed and managed through the favorites page.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** CocktailDB API

### Conclusion

The CocktailsAPI application provides a seamless experience for users to discover and manage their favorite cocktails. Built with Python, Flask and PostgreSQL, it leverages secure user authentication and dynamic content rendering to deliver a robust and user-friendly interface.

This project serves as a robust starting point for developing more complex web applications using Python, Flask, SQLAlchemy and PostgreSQL, with a clean structure and modular design for easy expansion and maintenance.
