from my_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(int(user_id))
    except:
        return None

class User(db.Model, UserMixin):

    __tablename__ = "shop_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()


class Orders(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("shop_users.id", ondelete="CASCADE"), nullable=False)
    #product_id = db.Column(db.Integer, db.ForeignKey("Products", ondelete="CASACADE"), nullable=False)
    producto = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_user(id):
        return Orders.query.filter_by(user_id=id).all()

    @staticmethod
    def get_all():
        return Orders.query.all()


# Run migrations
db.create_all()
