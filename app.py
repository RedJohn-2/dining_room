from model import Dish, Product, DishProduct, Provider, Menu, MenuDish
from app_config import app, db

from flask import request, render_template, redirect, url_for

from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product/<int:page_num>')
def products(page_num):
    data = db.session.query(Product). \
        order_by(Product.id). \
        paginate(per_page=25, page=page_num, error_out=True)

    return render_template('product.html', data=data, link='products')


@app.route('/product_sort/<int:page_num>')
def product_sort(page_num):
    data = db.session.query(Product). \
        order_by(Product.name). \
        paginate(per_page=25, page=page_num, error_out=True)

    return render_template('product.html', data=data, link='product_sort')


@app.route('/provider')
def providers():
    data = db.session.query(Provider). \
        order_by(Provider.id). \
        all()

    return render_template('provider.html', data=data)


@app.route('/provider_sort')
def provider_sort():
    data = db.session.query(Provider). \
        order_by(Provider.name). \
        all()

    return render_template('provider.html', data=data)


@app.route('/menu')
def menu():
    data = db.session.query(Menu). \
        order_by(Menu.id). \
        all()

    return render_template('menu.html', data=data)


@app.route('/menu_sort')
def menu_sort():
    data = db.session.query(Menu). \
        order_by(Menu.date_of_operation). \
        all()

    return render_template('menu.html', data=data)


@app.route('/dish')
def dishes():
    data = db.session.query(Dish). \
        order_by(Dish.id). \
        all()
    return render_template('dish.html', data=data)


@app.route('/dish_sort')
def dish_sort():
    data = db.session.query(Dish). \
        order_by(Dish.name). \
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


@app.route('/menu_dish')
def menu_and_dishes():
    data = db.session.query(MenuDish). \
        order_by(MenuDish.id_menu). \
        all()

    return render_template('menu_dish.html', data=data)


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


@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    menu = Menu()
    menu.date_of_operation = datetime.now()
    if request.method == 'GET':
        return render_template('add_menu.html', menu=menu)
    if request.method == 'POST':
        menu.date_of_operation = datetime.strptime(request.form['date'], "%Y-%m-%d")
        row = db.session.query(Menu).filter(Menu.date_of_operation == menu.date_of_operation).one_or_none()
        if row is not None:
            return "Error, this date already exist"
        db.session.add(menu)
        db.session.commit()
        db.session.flush()
        return redirect('/menu')


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
        return redirect('/product/1')


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
        row = db.session.query(DishProduct).filter(DishProduct.id_dish == dish_product.id_dish) \
            .filter(DishProduct.id_product == dish_product.id_product) \
            .one_or_none()
        if row is not None:
            return "Error, this entry already exist"
        dish_product.amount = float(request.form["amount"])
        db.session.add(dish_product)
        db.session.commit()
        db.session.flush()
        return redirect('/dish_product')


@app.route('/add_menu_dish', methods=['GET', 'POST'])
def add_menu_dish():
    menu_dish = MenuDish()
    if request.method == 'GET':
        dish = db.session.query(Dish). \
            order_by(Dish.id). \
            all()
        menu = db.session.query(Menu). \
            order_by(Menu.id). \
            all()
        return render_template('add_menu_dish.html', dish=dish, menu=menu, data=menu_dish)
    if request.method == 'POST':
        menu_dish.id_dish = int(request.form["id_dish"])
        menu_dish.id_menu = int(request.form["id_menu"])
        row = db.session.query(MenuDish).filter(MenuDish.id_dish == menu_dish.id_dish) \
            .filter(MenuDish.id_menu == menu_dish.id_menu) \
            .one_or_none()
        if row is not None:
            return "Error, this entry already exist"
        db.session.add(menu_dish)
        db.session.commit()
        db.session.flush()
        return redirect('/menu_dish')


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
    dish_product = db.session.query(DishProduct).filter(DishProduct.id_dish == id_dish) \
        .filter(DishProduct.id_product == id_product) \
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


@app.route('/update_menu/<int:id>', methods=['GET', 'POST'])
def update_menu(id):
    menu = db.session.query(Menu).filter(Menu.id == id).one_or_none()
    if menu is None:
        return 'Not Found', 404
    if request.method == 'GET':
        return render_template('add_menu.html', menu=menu)
    if request.method == 'POST':
        menu.date_of_operation = datetime.strptime(request.form['date'], "%Y-%m-%d")
        row = db.session.query(Menu).filter(Menu.date_of_operation == menu.date_of_operation).one_or_none()
        if row is not None:
            return "Error, this date already exist"
        db.session.add(menu)
        db.session.commit()
        return redirect('/menu')


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
        return redirect('/product/1')


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


@app.route('/delete_menu/<int:id>')
def delete_menu(id):
    menu = db.session.query(Menu).filter(Menu.id == id).one_or_none()
    if menu is not None:
        db.session.delete(menu)
        db.session.commit()
    return redirect('/menu')


@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = db.session.query(Product).filter(Product.id == id).one_or_none()
    if product is not None:
        db.session.delete(product)
        db.session.commit()
    return redirect('/product/1')


@app.route('/delete_dish_product/<int:id_dish>/<int:id_product>')
def delete_dish_product(id_dish, id_product):
    dish_product = db.session.query(DishProduct).filter(DishProduct.id_dish == id_dish) \
        .filter(DishProduct.id_product == id_product) \
        .one_or_none()
    if dish_product is not None:
        db.session.delete(dish_product)
        db.session.commit()
    return redirect('/dish_product')


@app.route('/delete_menu_dish/<int:id_menu>/<int:id_dish>')
def delete_menu_dish(id_menu, id_dish):
    menu_dish = db.session.query(MenuDish).filter(MenuDish.id_menu == id_menu) \
        .filter(MenuDish.id_dish == id_dish) \
        .one_or_none()
    if menu_dish is not None:
        db.session.delete(menu_dish)
        db.session.commit()
    return redirect('/menu_dish')


@app.route('/search_provider', methods=['GET', 'POST'])
def search_provider():
    if request.method == 'GET':
        return render_template('search_provider.html')
    if request.method == 'POST':
        name = request.form['name']
        # provider.hire_date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        data = db.session.query(Provider).filter(Provider.name.like("%" + name + "%")).order_by(Provider.id).all()
        if not data:
            return "Nothing not found!"
        return render_template('provider.html', data=data)


@app.route('/search_menu', methods=['GET', 'POST'])
def search_menu():
    if request.method == 'GET':
        return render_template('search_menu.html')
    if request.method == 'POST':
        date_begin = request.form['date_begin']
        date_end = request.form['date_end']
        query = db.session.query(Menu)

        if date_begin != '':
            query = query.filter(Menu.date_of_operation >= datetime.strptime(date_begin, "%Y-%m-%d"))

        if date_end != '':
            query = query.filter(Menu.date_of_operation < datetime.strptime(date_end, "%Y-%m-%d"))

        data = query.order_by(Menu.id).all()
        if not data:
            return "Nothing not found!"
        return render_template('menu.html', data=data)


@app.route('/search_dish_product', methods=['GET', 'POST'])
def search_dish_product():
    if request.method == 'GET':
        dish = db.session.query(Dish). \
            order_by(Dish.id). \
            all()
        product = db.session.query(Product). \
            order_by(Product.id). \
            all()
        return render_template('search_dish_product.html', dish=dish, product=product)
    if request.method == 'POST':
        id_dish = request.form["id_dish"]
        id_product = request.form["id_product"]
        query = db.session.query(DishProduct)
        if id_dish != '':
            query = query.filter(DishProduct.id_dish == int(id_dish))

        if id_product != '':
            query = query.filter(DishProduct.id_product == int(id_product))

        data = query.order_by(DishProduct.id_dish).all()
        if not data:
            return "Nothing not found!"
        return render_template('dish_product.html', data=data)


@app.route('/search_menu_dish', methods=['GET', 'POST'])
def search_menu_dish():
    if request.method == 'GET':
        dish = db.session.query(Dish). \
            order_by(Dish.id). \
            all()
        menu = db.session.query(Menu). \
            order_by(Menu.id). \
            all()
        return render_template('search_menu_dish.html', dish=dish, menu=menu)
    if request.method == 'POST':
        id_dish = request.form["id_dish"]
        id_menu = request.form["id_menu"]
        query = db.session.query(MenuDish)
        if id_dish != '':
            query = query.filter(MenuDish.id_dish == int(id_dish))

        if id_menu != '':
            query = query.filter(MenuDish.id_menu == int(id_menu))

        data = query.order_by(MenuDish.id_menu).all()
        if not data:
            return "Nothing not found!"
        return render_template('menu_dish.html', data=data)


@app.route('/search_dish', methods=['GET', 'POST'])
def search_dish():
    if request.method == 'GET':
        return render_template('search_dish.html')
    if request.method == 'POST':
        name = request.form['name']
        calorific_min = request.form['calorific_min']
        calorific_max = request.form['calorific_max']
        price_min = request.form['price_min']
        price_max = request.form['price_max']
        amount_min = request.form['amount_min']
        amount_max = request.form['amount_max']
        query = db.session.query(Dish).filter(Dish.name.like("%" + name + "%"))

        if calorific_min != '':
            query = query.filter(Dish.calorific >= float(calorific_min))

        if calorific_max != '':
            query = query.filter(Dish.calorific <= float(calorific_max))

        if price_min != '':
            query = query.filter(Dish.price >= float(price_min))

        if price_max != '':
            query = query.filter(Dish.price <= float(price_max))

        if amount_min != '':
            query = query.filter(Dish.amount >= int(amount_min))

        if amount_max != '':
            query = query.filter(Dish.amount <= int(amount_max))

        data = query.order_by(Dish.id).all()
        if not data:
            return "Nothing not found!"
        return render_template('dish.html', data=data)


@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    if request.method == 'GET':
        provider = db.session.query(Provider). \
            order_by(Provider.id). \
            all()
        return render_template('search_product.html', provider=provider)
    if request.method == 'POST':
        name = request.form['name']
        id_provider = int(request.form['id_provider'])
        amount_min = request.form['amount_min']
        amount_max = request.form['amount_max']
        query = db.session.query(Product).filter(Product.name.like("%" + name + "%"))

        if amount_min != '':
            query = query.filter(Product.amount >= int(amount_min))

        if amount_max != '':
            query = query.filter(Product.amount <= int(amount_max))

        if id_provider == 0:
            query = query.filter(Product.id_provider.is_(None))
        elif id_provider > 0:
            query = query.filter(Product.id_provider == id_provider)
        data = query.order_by(Product.id).all()
        if not data:
            return "Nothing not found!"
        return render_template('filtered_product.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
