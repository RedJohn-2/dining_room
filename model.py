from app_config import db


class Dish(db.Model):
    __tablename__ = 'dish'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    calorific = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.Text(), nullable=False)
    dish_ingredient = db.relationship("DishProduct", lazy=True, backref='dish', cascade="all", uselist=False)

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    id_provider = db.Column(db.Integer(), db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', back_populates="product")
    dish_ingredient = db.relationship("DishProduct", lazy=True, backref='product', cascade="all", uselist=False)

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class Provider(db.Model):
    __tablename__ = 'provider'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    hire_date = db.Column(db.Date(), nullable=False)
    product = db.relationship('Product', back_populates="provider")

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class DishProduct(db.Model):
    __tablename__ = 'dish_ingredient'
    id_dish = db.Column(db.Integer(), db.ForeignKey('dish.id'), primary_key=True)
    id_product = db.Column(db.Integer(), db.ForeignKey('product.id'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)