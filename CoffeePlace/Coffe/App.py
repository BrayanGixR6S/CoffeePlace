from flask import Flask, flash, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
import datetime
import re
cantidad = 1
costo = 1.0
# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User
app = Flask(__name__)

app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'coffeeplace'
mysql = MySQL(app)


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['Username'], request.form['Password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('escritorio'))
            else:
                flash("Invalid password...")
                return render_template('index.html')
        else:
            flash("User not found...")
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route("/escritorio")
def escritorio():
    return render_template("escritorio.html")

# Productos

@app.route('/productos')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()
    return render_template('productos.html', productos=data)


@app.route('/productos', methods=['POST'])
def productos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if not nombre:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('productos'))
        descripcion = request.form['descripcion']
        if not descripcion:
            flash('Por favor, ingrese una descripcion', 'error')
            return redirect(url_for('productos'))
        precio = request.form['precio']
        if not precio:
            flash('Por favor, ingrese el precio', 'error')
            return redirect(url_for('productos'))
        try:
            pattern = re.compile(r'^[a-zA-Z0-9_]+$')

            if bool(pattern.match(nombre)) is False:
                flash('El producto contiene caracteres especiales no permitidos', 'error')
                return redirect(url_for('productos'))

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT nombre FROM productos WHERE nombre = %s", (nombre,))
            nombreConsulta = cursor.fetchone()

            if nombreConsulta is not None:
                flash('El nombre del Producto ya esta registrado', 'error')
                return redirect(url_for('productos'))

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, descripcion, estado, precio) VALUES (%s,%s,%s,%s)", (nombre, descripcion, 1, precio))
            mysql.connection.commit()
            flash('Producto Añadido Correctamente', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('productos'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_productos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE productos_Id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_productos.html', productos=data[0])


@app.route('/productos/update/<id>', methods=['POST'])
def update_productos(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET nombre = %s,
                descripcion = %s,
                precio = %s
            WHERE productos_Id = %s
        """, (nombre, descripcion, precio, id,))
        flash('Registro actualizado', 'success')
        mysql.connection.commit()
        return redirect(url_for('productos'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_productos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE productos_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado Correctamente', "success")
    return redirect(url_for('productos'))

# Proveedores

@app.route('/proveedores')
def inicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedores')
    data = cur.fetchall()
    cur.close()
    return render_template('proveedores.html', proveedores=data)


@app.route('/proveedores', methods=['POST'])
def proveedores():
    if request.method == 'POST':
        nombre_pro = request.form['nombre_pro']
        if not nombre_pro:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('proveedores'))
        marca = request.form['marca']
        if not marca:
            flash('Por favor, ingrese la Marca del Proveedor', 'error')
            return redirect(url_for('proveedores'))
        domicilio = request.form['domicilio']
        if not domicilio:
            flash('Por favor, ingrese algun Domicilio', 'error')
            return redirect(url_for('proveedores'))
        telefono = request.form['telefono']
        if not domicilio:
            flash('Por favor, ingresa un Numero de Telefono', 'error')
            return redirect(url_for('proveedores'))
        try:
            pattern = re.compile(r'^[a-zA-Z0-9_]+$')

            if bool(pattern.match(nombre_pro)) is False:
                flash('La cadena contiene caracteres no permitidos', 'error')
                return redirect(url_for('proveedores'))
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO proveedores (nombre_pro, marca, estado_pro, domicilio, telefono) VALUES (%s,%s,%s,%s,%s)", (nombre_pro, marca, 1, domicilio, telefono))
            mysql.connection.commit()
            flash('Proveedor Añadido Correctamente', 'success')
            return redirect(url_for('proveedores'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('proveedores'))


@app.route('/proveedores/edit/<id>', methods=['POST', 'GET'])
def get_proveedores(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedores WHERE proveedores_Id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_proveedores.html', proveedores=data[0])


@app.route('/proveedores/update/<id>', methods=['POST'])
def update_proveedores(id):
    if request.method == 'POST':
        nombre_pro = request.form['nombre_pro']
        marca = request.form['marca']
        domicilio = request.form['domicilio']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE proveedores
            SET nombre_pro = %s,
                marca = %s,
                domicilio = %s,
                telefono = %s
            WHERE proveedores_Id = %s
        """, (nombre_pro, marca, domicilio, telefono, id,))
        flash('Proveedor Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('proveedores'))


@app.route('/proveedores/delete/<string:id>', methods=['POST', 'GET'])
def delete_proveedores(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'DELETE FROM proveedores WHERE proveedores_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Proveedor Eliminado Correctamente', 'success')
    return redirect(url_for('proveedores'))

# Usuarios
@app.route('/usuarios')
def usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=data)

@app.route('/usuarios', methods=['POST'])
def user():
    if request.method == 'POST':
        username = request.form['username']
        if not username:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('usuarios'))
        password = request.form['password']
        if not password:
            flash('Por favor, ingrese una contraseña', 'error')
            return redirect(url_for('usuarios'))
        fullname = request.form['fullname']
        if not fullname:
            flash('Por favor, ingrese el nombre del Usuario', 'error')
            return redirect(url_for('usuarios'))
        try:
            pattern = re.compile(r'^[a-zA-Z0-9_]+$')

            if bool(pattern.match(username)) is False:
                flash('La cadena contiene caracteres no permitidos', 'error')
                return redirect(url_for('usuario'))
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO user (username, password, fullname) VALUES (%s,%s,%s)", (username, password, fullname))
            mysql.connection.commit()
            flash('Usuario Añadido Correctamente', 'success')
            return redirect(url_for('usuarios'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('usuarios'))
        
@app.route('/usuarios/delete/<string:id>', methods=['POST', 'GET'])
def delete_usuarios(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'DELETE FROM user WHERE user_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario Eliminado Correctamente', 'success')
    return redirect(url_for('usuarios'))

# Materias Primas

@app.route('/materias_primas')
def inicio1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias_primas')
    data = cur.fetchall()
    cur.close()
    return render_template('materiasprimas.html', materiasprimas=data)


@app.route('/materias_primas', methods=['POST'])
def materiasprimas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if not nombre:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('materiasprimas'))
        descripcion = request.form['descripcion']
        if not descripcion:
            flash('Por favor, ingrese una descripcion', 'danger')
            return redirect(url_for('materiasprimas'))
        precio = request.form['precio']
        if not precio:
            flash('Por favor, ingrese el precio', 'danger')
            return redirect(url_for('materiasprimas'))
        try:
            pattern = re.compile(r'^[a-zA-Z0-9_]+$')

            if bool(pattern.match(nombre)) is False:
                flash('La cadena contiene caracteres no permitidos', 'danger')
                return redirect(url_for('materiasprimas'))
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO materias_primas (nombre, descripcion, precio, existencia) VALUES (%s,%s,%s,%s)", (nombre, descripcion, precio, 1))
            mysql.connection.commit()
            flash('Materia_Prima Añadida Correctamente', 'success')
            return redirect(url_for('materiasprimas'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('materiasprimas'))
        

@app.route('/materiasprimas/edit/<id>', methods=['POST', 'GET'])
def get_materiasprimas(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias_primas WHERE materias_primas_Id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_materias_primas.html', materias_primas=data[0])

@app.route('/materiasprimas/update/<id>', methods=['POST'])
def update_materiasprimas(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE materias_primas
            SET nombre = %s,
                descripcion = %s,
                precio = %s
            WHERE materias_primas_Id = %s
        """, (nombre, descripcion, precio, id))
        flash('Materia_Prima Editada Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('materiasprimas'))
    
@app.route('/materiasprimas/delete/<string:id>', methods=['POST', 'GET'])
def delete_materiasprimas(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'DELETE FROM materias_primas WHERE materias_primas_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Materia_Prima Eliminada Correctamente', 'success')
    return redirect(url_for('materiasprimas'))

@app.route('/puntoventa')
def puntoventa():
    return render_template('puntoventa.html')

@app.route('/puntoventa/agregar/carrito/<id>')
def puntoventaAgregarCarrito(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE productos_Id = %s',(id,))
    producto = cur.fetchone()
    cur.close()

    if producto is None:
        flash('No se encontro el producto', 'danger')
    
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, producto in enumerate(carrito):
            if producto[0] == id:
                carrito[i] = (producto[0], producto[1] + 1)  # Aumentar la cantidad en 1
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if not encontrado:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("puntoventa"))

@app.route('/puntoventa/finalizar-venta')
def puntoventaFinalizarVenta():
    # Verificar si el carrito está vacío
    if "carrito" not in session or len(session["carrito"]) == 0:
        flash('El carrito está vacío', 'error')
        return redirect(url_for("puntoventa"))

    # Obtener el ID del empleado de la sesión
    empleado_id = session.get("empleado_Id")

    # Obtener el total de la venta
    total = 0
    cur = mysql.connection.cursor()
    for producto in session["carrito"]:
        producto_id = producto[0]
        cantidad = producto[1]
        cur.execute("SELECT precio FROM productos WHERE productos_Id = %s", (producto_id,))
        precio = cur.fetchone()
        if precio is None:
            flash(f'No se encontró el precio del producto {producto_id}', 'error')
            cur.close()
            return redirect(url_for("puntoventa"))
        total += cantidad * precio[0]

    cur.close()

    if total <= 0:
        flash('El carrito está vacío', 'error')
        return redirect(url_for("puntoventa"))

    # Crear una nueva transacción SQL
    cur = mysql.connection.cursor()

    try:
        # Iniciar la transacción
        cur.execute("START TRANSACTION")

        # Insertar la nueva venta en la tabla 'venta'
        cur.execute("INSERT INTO venta (empleadosFK, fecha, hora, venta_total) VALUES (%s, NOW(), NOW(), %s)", (empleado_id, total))
        # Obtener el ID de la venta recién insertada
        venta_id = cur.lastrowid

        # Insertar los detalles de la venta en la tabla 'det_venta'
        for producto in session["carrito"]:
            producto_id = producto[0]
            cantidad = producto[1]
            cur.execute("SELECT precio FROM productos WHERE productos_Id = %s", (producto_id,))
            precio = cur.fetchone()
            if precio is None:
                flash(f'No se encontró el precio del producto {producto_id}', 'error')
                cur.execute("ROLLBACK")
                cur.close()
                return redirect(url_for("puntoventa"))
            importe = cantidad * precio[0]
            cur.execute("INSERT INTO det_venta (productosFK, precio, cantidad, importe, ventaFK) VALUES (%s, %s, %s, %s, %s)", (producto_id, precio[0], cantidad, importe, venta_id))

        # Confirmar la transacción
        cur.execute("COMMIT")

        # Vaciar el carrito de la sesión
        session["carrito"] = []

        # Redirigir al punto de venta con un mensaje de éxito
        flash('Venta finalizada con éxito', 'success')
        return redirect(url_for("puntoventaTicketVenta",venta_id=venta_id))

    except Exception as e:
        # Deshacer la transacción en caso de error
        cur.execute("ROLLBACK")
        return "Error al finalizar la venta: " + str(e)

    finally:
        cur.close()      

@app.route('/puntoventa/eliminar/carrito/<id>')
def puntoventaEliminarCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, producto in enumerate(carrito):
            if producto[0] == id:
                del carrito[i]  # Eliminar la tupla correspondiente del carrito
                encontrado = True
                break

        # Si no se encontró el producto, mostrar un mensaje de error
        if not encontrado:
            return "El producto no está en el carrito"

        session["carrito"] = carrito

    return redirect(url_for("puntoventa"))

@app.route('/puntoventa/aumenta/carrito/<id>')
def puntoventaAumentaCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, producto in enumerate(carrito):
            if producto[0] == id:
                carrito[i] = (producto[0], producto[1] + 1)  # Aumentar la cantidad en 1
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if not encontrado:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("puntoventa"))


@app.route('/puntoventa/disminuye/carrito/<id>')
def catalogodisminuyeCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, producto in enumerate(carrito):
            if producto[0] == id:
                if producto[1] <= 0:
                    flash('El producto ya tiene una cantidad de 0')
                    encontrado = True
                    break
                carrito[i] = (producto[0], producto[1] - 1)  # Disminuye la cantidad en 1
                if producto[1] == 1:
                    del carrito[i]
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if encontrado is False:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("carrito"))


@app.route('/consulta/producto', methods=['POST', 'GET'])
def consulta():
    busqueda = request.form['busqueda']
    like = f"%{busqueda}%"

    cur = mysql.connection.cursor()
    cur.execute('SELECT productos_Id, nombre, descripcion, precio FROM productos WHERE productos_Id LIKE %s OR nombre LIKE %s OR descripcion LIKE %s',(like,like,like,))
    importe = costo * cantidad
    productos = cur.fetchall()
    cur.close()
    return render_template('tabla_productos.html', productos=productos, importe=importe)

@app.route('/consulta/carrito', methods=['POST', 'GET'])
def consultaCarrito():
    carrito = session["carrito"]
    producto = []
    
    total = 0
    for producto in carrito:
        id = producto[0]
        cantidad = producto[1]

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE productos_Id = %s',(id,))
        prod = cur.fetchone()
        cur.close()

        res = {
            "id": id,
            "nombre": prod[1],
            "descripcion": prod[2],
            "precio": prod[4],
            "cantidad": cantidad,
            "importe": prod[4] * cantidad
        }
        productos.append(res)

        total = total + prod[4] * cantidad
        
    return render_template("/tabla_carrito.html", productos = productos, total = total)


@app.route('/puntoventa/ticket-venta/<int:venta_id>')
def puntoventaTicketVenta(venta_id):
    # Obtener los detalles de la venta
    cur = mysql.connection.cursor()
    cur.execute("SELECT productos.nombre, productos.descripcion, det_venta.cantidad, det_venta.precio, det_venta.importe FROM det_venta INNER JOIN productos ON det_venta.productosFK = productos.productos_Id WHERE det_venta.ventaFK = %s", (venta_id,))
    productos = cur.fetchall()

    # Obtener el total de la venta
    cur.execute("SELECT venta_total FROM venta WHERE venta_Id = %s", (venta_id,))
    total = cur.fetchone()[0]

    # Renderizar el HTML del ticket de venta con los datos de la venta
    return render_template("ticket.html", productos=productos, total=total, folio=venta_id)



@app.route('/validar Caracteres especiales', methods=['POST'])
def validar_Caracteres():
    cadena = request.form['cadena']
    pattern = re.compile(r'^\w+$')

    if pattern.match(cadena):
        return 'La cadena es válida'
    else:
        flash('La cadena contiene caracteres no permitidos')


# Validaciones

@app.route('/validar', methods=['POST'])
def validar():
    # Código para validar los datos
    if validar():
        mensaje = 'Los datos son válidos'
        tipo = 'success'
    else:
        mensaje = 'Los datos son inválidos'
        tipo = 'error'

    # Devolver la respuesta en formato JSON
    return jsonify({'mensaje': mensaje, 'tipo': tipo})


@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
