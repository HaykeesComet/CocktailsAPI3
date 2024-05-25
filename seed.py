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
