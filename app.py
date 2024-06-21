from flask import Flask, render_template, request, redirect, url_for, flash
from model import db, Producto
import controller
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = controller.get_all_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = controller.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/create', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        controller.create_product(nombre, descripcion, precio)
        flash('Producto creado con éxito!')
        return redirect(url_for('index'))
    return render_template('product_form.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = controller.get_product_by_id(product_id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        controller.update_product(product_id, nombre, descripcion, precio)
        flash('¡Producto actualizado exitosamente!')
        return redirect(url_for('index'))
    return render_template('product_form.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    controller.delete_product(product_id)
    flash('Producto eliminado exitosamente!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
