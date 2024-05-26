from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
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
    
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favorite.query.filter_by(user_id=current_user.id, drink_id=drink_id).first() is not None
    
    return render_template('drink.html', drink=drink, is_favorited=is_favorited)

@drinks_bp.route('/favorite/<drink_id>', methods=['POST'])
@login_required
def favorite(drink_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, drink_id=drink_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}')
        drink = response.json().get('drinks')[0]
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
