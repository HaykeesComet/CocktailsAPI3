# drinks.py
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from flask_login import login_required, current_user
from models import db, Favorite

drinks_bp = Blueprint('drinks', __name__)

COCKTAIL_API_URL = 'https://www.thecocktaildb.com/api/json/v1/1'

@drinks_bp.route('/')
def index():
    return render_template('index.html')

@drinks_bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        try:
            response = requests.get(f'{COCKTAIL_API_URL}/search.php?s={query}')
            response.raise_for_status()  # Raises an error for bad status codes
            drinks = response.json().get('drinks')
        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching drinks: {e}")
            flash('There was an error contacting the drink API. Please try again later.', 'error')
            drinks = None
        return render_template('index.html', drinks=drinks)
    return redirect(url_for('drinks.index'))

@drinks_bp.route('/drink/<drink_id>')
def drink(drink_id):
    try:
        response = requests.get(f'{COCKTAIL_API_URL}/lookup.php?i={drink_id}')
        response.raise_for_status()  # Raises an error for bad status codes
        drink = response.json().get('drinks')[0]
    except requests.RequestException as e:
        current_app.logger.error(f"Error fetching drink details: {e}")
        flash('There was an error contacting the drink API. Please try again later.', 'error')
        return redirect(url_for('drinks.index'))
    
    ingredients = [(drink.get(f'strIngredient{i}'), drink.get(f'strMeasure{i}')) for i in range(1, 16) if drink.get(f'strIngredient{i}')]

    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favorite.query.filter_by(user_id=current_user.id, drink_id=drink_id).first() is not None
    
    return render_template('drink.html', drink=drink, ingredients=ingredients, is_favorited=is_favorited)

@drinks_bp.route('/favorite/<drink_id>', methods=['POST'])
@login_required
def favorite(drink_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, drink_id=drink_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        try:
            response = requests.get(f'{COCKTAIL_API_URL}/lookup.php?i={drink_id}')
            response.raise_for_status()  # Raises an error for bad status codes
            drink = response.json().get('drinks')[0]
        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching drink details for favorite: {e}")
            flash('There was an error contacting the drink API. Please try again later.', 'error')
            return jsonify({'status': 'error'}), 500
        
        new_favorite = Favorite(user_id=current_user.id, drink_id=drink_id, drink_name=drink['strDrink'], drink_image=drink['strDrinkThumb'])
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'status': 'added'})

@drinks_bp.route('/is_favorited/<drink_id>', methods=['GET'])
@login_required
def is_favorited(drink_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, drink_id=drink_id).first()
    return jsonify({'favorited': favorite is not None})

@drinks_bp.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites, current_user=current_user)
