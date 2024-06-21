# CRUD Productos

## Descripción.

Esta es una aplicación sencilla para el manejo de base de datos usando el Framework para Python llamado Flask y SQLite cómo base de datos

| Tabla de Contenidos.              |
| :-------------------------------- |
| [Instalación](#instalación)       |
| [Funcionamiento](#funcionamiento) |
| [Uso](#uso)                       |

## Instalación.

### Requisitos de instalación.

- Python 3.+
- Flask
- pip (gestor de paquetes de Python)

### Paso a Paso.

1. **Clonar el repositorio**
   `git clone https://github.com/EmelDMedina/CRUD-Productos.git`
2. **Instalar un Entorno Virtual (opcional)** Si desea instalar un entorno virtual para no afectar las dependencias en su computadora, lo puede hacer usando el siguiente comando en la consola.

   ```bash
   $ pip install virtualenv
   $ python -m virtualenv env
   $ env\Scripts\activate
   ```

3. **Instalar las dependencias** `pip install -r requirements.txt`

## Funcionamiento.

| Archivos y su funcionamiento   |
| :----------------------------- |
| [app.py](#apppy)               |
| [config.py](#configpy)         |
| [controller.py](#controllerpy) |
| [model.py](#modelpy)           |
| [resumen](#resumen)            |

### app.py

#### 1. Importaciones.

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from model import db, Producto
import controller
from config import Config
```

- **Flask**: El marco de trabajo para crear aplicaciones web.
- **render_template**: Para renderizar plantillas HTML.
- **request**: Para manejar solicitudes HTTP.
- **redirect**: Para redirigir a otra URL.
- **url_for**: Para construir URLs basadas en el nombre de la función de vista.
- **flash**: Para mostrar mensajes en la aplicación web.
- **db** y **Producto**: Importados del módulo `model`, representan la base de datos y el modelo de producto.
- **controller**: Un módulo personalizado para manejar la lógica de negocio.
- **Config**: Importado del módulo `config`, contiene la configuración de la aplicación.

#### 2. Configuración de la aplicación Flask

```python
app = Flask(__name__)
app.config.from_object(Config)
```

- Se crea una instancia de la aplicación Flask.
- Se configura la aplicación usando la configuración definida en `Config`.

#### 3. Inicialización de la base de datos

```python
db.init_app(app)

with app.app_context():
    db.create_all()
```

- Se inicializa la base de datos con la aplicación Flask.
- Se crea el contexto de la aplicación para asegurarse de que la base de datos se crea dentro del contexto de la aplicación.

#### 4. Rutas de la aplicación

- ##### Ruta principal

  ```python
  @app.route('/')
  def index():
      products = controller.get_all_products()
      return render_template('index.html', products=products)
  ```

  - Muestra todos los productos en la página principal.
  - Usa la función `get_all_products` del controlador para obtener todos los productos.
  - Renderiza la plantilla `index.html` con la lista de productos.

- ##### Detalle del producto

  ```python
  @app.route('/product/<int:product_id>')
  def product_detail(product_id):
      product = controller.get_product_by_id(product_id)
      return render_template('product_detail.html', product=product)
  ```

  - Muestra los detalles de un producto específico.
  - Usa la función `get_product_by_id` del controlador para obtener el producto por su ID.
  - Renderiza la plantilla `product_detail.html` con los detalles del producto.

- ##### Crear producto

  ```python
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
  ```

  - Permite crear un nuevo producto.
  - Si el método es `POST`, obtiene los datos del formulario, crea el producto y redirige a la página principal.
  - Si el método es `GET`, muestra el formulario para crear el producto.

- ##### Editar producto

  ```python
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
  ```

  - Permite editar un producto existente.
  - Si el método es `POST`, actualiza los datos del producto y redirige a la página principal.
  - Si el método es `GET`, muestra el formulario con los datos del producto para editarlos.

- ##### Eliminar producto

  ```python
  @app.route('/delete_product/<int:product_id>')
  def delete_product(product_id):
      controller.delete_product(product_id)
      flash('Producto eliminado exitosamente!')
      return redirect(url_for('index'))
  ```

  - Permite eliminar un producto.
  - Usa la función `delete_product` del controlador para eliminar el producto por su ID.
  - Redirige a la página principal y muestra un mensaje de éxito.

#### 5. Ejecución de la aplicación

```python
if __name__ == '__main__':
    app.run(debug=True)
```

- Inicia la aplicación Flask en modo debug si el script se ejecuta directamente.

### config.py

#### 1. **Importación del módulo `os`**

```python
import os
```

**os**: Es un módulo que proporciona una forma de usar funcionalidades dependientes del sistema operativo, como leer o escribir en el sistema de archivos.

#### 2. **Definición de la clase `Config`**: Se define una clase llamada `Config` que se utiliza para almacenar configuraciones de la aplicación.

#### 3. **Atributo `SECRET_KEY`**

```python
SECRET_KEY = os.urandom(24)
```

- **SECRET_KEY**: Es una clave secreta que se usa para mantener seguras las sesiones y otros datos sensibles en la aplicación Flask.
- **os.urandom(24)**: Genera una cadena de 24 bytes aleatorios, lo que proporciona una clave secreta única cada vez que se inicia la aplicación.

#### 4. **Atributo `SQLALCHEMY_DATABASE_URI`**

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(os.getcwd(), 'db', 'app.db'))
```

- **SQLALCHEMY_DATABASE_URI**: Especifica la URI de la base de datos que SQLAlchemy usará para conectarse.
- **sqlite:///{}**: Define una base de datos SQLite que se almacenará en un archivo.
- **os.path.join(os.getcwd(), 'db', 'app.db')**: Construye la ruta al archivo de la base de datos. Usa el directorio actual de trabajo (`os.getcwd()`), crea una subcarpeta llamada `db`, y dentro de esa subcarpeta crea o usa un archivo llamado `app.db`.

#### 5. **Atributo `SQLALCHEMY_TRACK_MODIFICATIONS`**

```python
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

- **SQLALCHEMY_TRACK_MODIFICATIONS**: Esta configuración desactiva la característica de seguimiento de modificaciones de objetos, que consume memoria adicional. Configurarlo como `False` es una práctica común para mejorar el rendimiento y evitar advertencias innecesarias.

### controller.py

#### 1. **Importación de `db` y `Producto`**

```python
from model import db, Producto
```

- **db**: Es la instancia de la base de datos SQLAlchemy.
- **Producto**: Es el modelo de datos que representa un producto en la base de datos.

#### 2. **Funciones para manejar productos**

- ##### Crear un producto

  ```python
  def create_product(nombre, descripcion, precio):
      new_product = Producto(nombre=nombre, descripcion=descripcion, precio=precio)
      db.session.add(new_product)
      db.session.commit()
      return new_product
  ```

  - **create_product(nombre, descripcion, precio)**: Crea un nuevo producto con el nombre, descripción y precio proporcionados.
  - **new_product**: Se instancia un nuevo objeto `Producto` con los datos proporcionados.
  - **db.session.add(new_product)**: Se agrega el nuevo producto a la sesión de la base de datos.
  - **db.session.commit()**: Se guarda el nuevo producto en la base de datos.
  - **return new_product**: Devuelve el producto creado.

- ##### **Obtener todos los productos**

  ```python
  def get_all_products():
      return Producto.query.all()
  ```

  - **get_all_products()**: Obtiene y devuelve todos los productos almacenados en la base de datos.
  - **Producto.query.all()**: Realiza una consulta para obtener todos los registros de la tabla `Producto`.

- ##### 4. Obtener un producto por ID

  ```python
  def get_product_by_id(product_id):
      return Producto.query.get(product_id)
  ```

  - **get_product_by_id(product_id)**: Obtiene y devuelve un producto específico basado en su ID.
  - **Producto.query.get(product_id)**: Realiza una consulta para obtener el producto con el ID especificado.

- ##### Actualizar un producto

  ```python
  def update_product(product_id, nombre, descripcion, precio):
      product = Producto.query.get(product_id)
      if product:
          product.nombre = nombre
          product.descripcion = descripcion
          product.precio = precio
          db.session.commit()
          return product
  return None
  ```

  - **update_product(product_id, nombre, descripcion, precio)**: Actualiza los datos de un producto existente.
  - **product = Producto.query.get(product_id)**: Obtiene el producto con el ID especificado.
  - **if product:**: Verifica si el producto existe.
  - **product.nombre = nombre**: Actualiza el nombre del producto.
  - **product.descripcion = descripcion**: Actualiza la descripción del producto.
  - **product.precio = precio**: Actualiza el precio del producto.
  - **db.session.commit()**: Guarda los cambios en la base de datos.
  - **return product**: Devuelve el producto actualizado.
  - **return None**: Si el producto no existe, devuelve `None`.

- ##### Eliminar un producto
  ```python
  def delete_product(product_id):
      product = Producto.query.get(product_id)
      if product:
          db.session.delete(product)
          db.session.commit()
          return True
      return False
  ```
  - **delete_product(product_id)**: Elimina un producto existente de la base de datos.
    - **product = Producto.query.get(product_id)**: Obtiene el producto con el ID especificado.
    - **if product:**: Verifica si el producto existe.
      - **db.session.delete(product)**: Marca el producto para eliminación.
      - **db.session.commit()**: Elimina el producto de la base de datos.
      - **return True**: Si la eliminación fue exitosa, devuelve `True`.
    - **return False**: Si el producto no existe, devuelve `False`.

### model.py

#### 1. **Importación de `SQLAlchemy`**

```python
from flask_sqlalchemy import SQLAlchemy
```

- **SQLAlchemy**: Es un ORM (Object Relational Mapper) para Python que permite interactuar con bases de datos de manera más intuitiva y con menos código SQL.

#### 2. **Creación de la instancia de la base de datos**

```python
db = SQLAlchemy()
```

- **db**: Se crea una instancia de `SQLAlchemy`, que se usará para interactuar con la base de datos en la aplicación Flask.

#### 3. **Definición de la clase `Producto`**

```python
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'
```

- **class Producto(db.Model)**: Define un modelo de datos llamado `Producto` que hereda de `db.Model`, lo que indica que esta clase es un modelo de SQLAlchemy.

#### 4. **Atributos de la clase `Producto`**

```python
id = db.Column(db.Integer, primary_key=True)
```

- **id**: Es un campo de tipo entero que actúa como clave primaria. Cada producto tendrá un ID único.

```python
nombre = db.Column(db.String(100), nullable=False)
```

- **nombre**: Es un campo de tipo cadena de caracteres con un máximo de 100 caracteres. No puede ser nulo, por lo que es obligatorio proporcionar un nombre para cada producto.

```python
descripcion = db.Column(db.Text, nullable=True)
```

- **descripcion**: Es un campo de tipo texto que puede almacenar descripciones largas. Es opcional, por lo que puede ser nulo.

```python
precio = db.Column(db.Float, nullable=False)
```

- **precio**: Es un campo de tipo flotante que almacena el precio del producto. No puede ser nulo, por lo que es obligatorio proporcionar un precio para cada producto.

#### 5. **Método `__repr__`**

```python
def __repr__(self):
    return f'<Producto {self.nombre}>'
```

- **`__repr__`**: Es un método especial que define cómo se representa el objeto `Producto` como una cadena. Esto es útil para depuración y logging. En este caso, devuelve una cadena que incluye el nombre del producto.

### Resumen

- **app.py**: Este archivo configura una aplicación web usando Flask que permite crear, leer, actualizar y eliminar productos, con vistas y plantillas HTML para interactuar con el usuario.
- **config.py**: Este archivo define una clase `Config` que se usa para configurar una aplicación Flask. Proporciona una clave secreta para la seguridad de la aplicación, configura la URI de la base de datos para usar SQLite y desactiva el seguimiento de modificaciones de objetos en SQLAlchemy para mejorar el rendimiento.
- **controller.py**: Este conjunto de funciones proporciona una interfaz para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos para la entidad `Producto`. Cada función se encarga de una operación específica utilizando SQLAlchemy para interactuar con la base de datos.
- **model.py**: Este archivo define un modelo de datos `Producto` para una aplicación Flask que utiliza SQLAlchemy como ORM. El modelo `Producto` tiene cuatro atributos: `id` (clave primaria), `nombre`, `descripcion` y `precio`. Cada uno de estos atributos se mapea a una columna en la tabla `Producto` en la base de datos. El método `__repr__` proporciona una representación legible del objeto `Producto` para facilitar la depuración.
