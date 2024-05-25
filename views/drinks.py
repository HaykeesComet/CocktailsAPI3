from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
import requests
from models import db, Favorite

drinks_bp = Blueprint('drinks', __name__)

@drinks_bp.route('/')
def index():
    return render_template('index.html')

@drinks_bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}')
        drinks = response.json().get('drinks')
        return render_template('index.html', drinks=drinks)
    return redirect(url_for('drinks.index'))

@drinks_bp.route('/drink/<drink_id>')
def drink(drink_id):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}')
    drink = response.json().get('drinks')[0]
    return render_template('drink.html', drink=drink)

@drinks_bp.route('/favorite/<drink_id>', methods=['POST'])
@login_required
def favorite(drink_id):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}')
    drink = response.json().get('drinks')[0]
    favorite = Favorite(user_id=current_user.id, drink_id=drink_id, drink_name=drink['strDrink'], drink_image=drink['strDrinkThumb'])
    db.session.add(favorite)
    db.session.commit()
    return redirect(url_for('drinks.index'))

@drinks_bp.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites, current_user=current_user)
