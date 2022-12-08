from model import Dish, Product, DishProduct, Provider
from app_config import app, db

from flask import request, render_template, redirect, url_for

from sqlalchemy import desc

from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product')
def products():
    data = db.session.query(Product). \
        order_by(Product.id). \
        all()

    return render_template('product.html', data=data)


@app.route('/provider')
def providers():
    data = db.session.query(Provider). \
        order_by(Provider.id). \
        all()

    return render_template('provider.html', data=data)


@app.route('/dish')
def dishes():
    data = db.session.query(Dish). \
        order_by(Dish.id). \
        all()
    return render_template('dish.html', data=data)


@app.route('/dish/<int:id>')
def dishes_recipe(id):
    dish = db.session.query(Dish).filter(Dish.id == id).one_or_none()
    if dish is None:
        return 'Not Found', 404
    return render_template('recipe.html', recipe=dish.recipe)


@app.route('/dish_product')
def dishes_and_products():
    data = db.session.query(DishProduct). \
        order_by(DishProduct.id_dish). \
        all()

    return render_template('dish_product.html', data=data)


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    dish = Dish()
    if request.method == 'GET':
        return render_template('add_dish.html', dish=dish)
    if request.method == 'POST':
        dish.name = request.form['name']
        dish.calorific = float(request.form['calorific'])
        dish.price = float(request.form['price'])
        dish.amount = int(request.form['amount'])
        dish.recipe = request.form['recipe']
        db.session.add(dish)
        db.session.commit()
        db.session.flush()
        return redirect('/dish')


@app.route('/add_provider', methods=['GET', 'POST'])
def add_provider():
    provider = Provider()
    provider.hire_date = datetime.now()
    if request.method == 'GET':
        return render_template('add_provider.html', provider=provider)
    if request.method == 'POST':
        provider.name = request.form['name']
        provider.hire_date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        db.session.add(provider)
        db.session.commit()
        db.session.flush()
        return redirect('/provider')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    product = Product()
    if request.method == 'GET':
        provider = db.session.query(Provider). \
        order_by(Provider.id). \
        all()
        return render_template('add_product.html', provider=provider, product=product)
    if request.method == 'POST':
        product.name = request.form["name"]
        product.amount = float(request.form["amount"])
        if int(request.form["id_provider"]) != 0:
            product.id_provider = int(request.form["id_provider"])
        db.session.add(product)
        db.session.commit()
        db.session.flush()
        return redirect('/product')


@app.route('/add_dish_product', methods=['GET', 'POST'])
def add_dish_product():
    dish_product = DishProduct()
    if request.method == 'GET':
        dish = db.session.query(Dish). \
            order_by(Dish.id). \
            all()
        product = db.session.query(Product). \
            order_by(Product.id). \
            all()
        return render_template('add_dish_product.html', dish=dish, product=product, data=dish_product)
    if request.method == 'POST':
        dish_product.id_dish = int(request.form["id_dish"])
        dish_product.id_product = int(request.form["id_product"])
        row = db.session.query(DishProduct).filter(DishProduct.id_dish == dish_product.id_dish)\
            .filter(DishProduct.id_product == dish_product.id_product)\
            .one_or_none()
        if row is not None:
            return "Error, this entry already exist"
        dish_product.amount = float(request.form["amount"])
        db.session.add(dish_product)
        db.session.commit()
        db.session.flush()
        return redirect('/dish_product')


@app.route('/update_dish/<int:id>', methods=['GET', 'POST'])
def update_dish(id):
    dish = db.session.query(Dish).filter(Dish.id == id).one_or_none()
    if dish is None:
        return 'Not Found', 404
    if request.method == 'GET':
        return render_template('add_dish.html', dish=dish)
    if request.method == 'POST':
        dish.name = request.form['name']
        dish.calorific = float(request.form['calorific'])
        dish.price = float(request.form['price'])
        dish.amount = int(request.form['amount'])
        dish.recipe = request.form['recipe']
        db.session.add(dish)
        db.session.commit()
        return redirect('/dish')


@app.route('/update_dish_product/<int:id_dish>/<int:id_product>', methods=['GET', 'POST'])
def update_dish_product(id_dish, id_product):
    dish_product = db.session.query(DishProduct).filter(DishProduct.id_dish == id_dish)\
            .filter(DishProduct.id_product == id_product)\
            .one_or_none()
    if dish_product is None:
        return "Not found", 404
    if request.method == 'GET':
        dish = (dish_product.dish,)
        product = (dish_product.product,)
        return render_template('add_dish_product.html', dish=dish, product=product, data=dish_product)
    if request.method == 'POST':
        dish_product.amount = float(request.form["amount"])
        db.session.add(dish_product)
        db.session.commit()
        return redirect('/dish_product')


@app.route('/update_provider/<int:id>', methods=['GET', 'POST'])
def update_provider(id):
    provider = db.session.query(Provider).filter(Provider.id == id).one_or_none()
    if provider is None:
        return 'Not Found', 404
    if request.method == 'GET':
        return render_template('add_provider.html', provider=provider)
    if request.method == 'POST':
        provider.name = request.form['name']
        provider.hire_date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        db.session.add(provider)
        db.session.commit()
        return redirect('/provider')


@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = db.session.query(Product).filter(Product.id == id).one_or_none()
    if product is None:
        return 'Not Found', 404
    if request.method == 'GET':
        provider = db.session.query(Provider). \
            order_by(Provider.id). \
            all()
        return render_template('add_product.html', provider=provider, product=product)
    if request.method == 'POST':
        product.name = request.form["name"]
        product.amount = float(request.form["amount"])
        if int(request.form["id_provider"]) != 0:
            product.id_provider = int(request.form["id_provider"])
        else:
            product.id_provider = None

        db.session.add(product)
        db.session.commit()
        return redirect('/product')


@app.route('/delete_dish/<int:id>')
def delete_dish(id):
    dish = db.session.query(Dish).filter(Dish.id == id).one_or_none()
    if dish is not None:
        db.session.delete(dish)
        db.session.commit()
    return redirect('/dish')


@app.route('/delete_provider/<int:id>')
def delete_provider(id):
    provider = db.session.query(Provider).filter(Provider.id == id).one_or_none()
    if provider is not None:
        db.session.delete(provider)
        db.session.commit()
    return redirect('/provider')


@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = db.session.query(Product).filter(Product.id == id).one_or_none()
    if product is not None:
        db.session.delete(product)
        db.session.commit()
    return redirect('/product')


@app.route('/delete_dish_product/<int:id_dish>/<int:id_product>')
def delete_dish_product(id_dish, id_product):
    dish_product = db.session.query(DishProduct).filter(DishProduct.id_dish == id_dish) \
        .filter(DishProduct.id_product == id_product) \
        .one_or_none()
    if dish_product is None:
        db.session.delete(dish_product)
        db.session.commit()
    return redirect('/dish_product')


if __name__ == '__main__':
    app.run(debug=True)
