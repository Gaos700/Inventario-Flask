import os
from flask import Flask,render_template,request,redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseInventario.db'
def get_db_connection():
    connection = sqlite3.connect('databaseInventario.db') #conexion a la base de datos
    connection.row_factory = sqlite3.Row #muestra los datos como objetos de fila en lugar de tuplas
    return connection


@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    cursor.execute('SELECT * FROM productos')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', datas = data)

@app.route('/add_product', methods = ['POST', 'GET'])
def add_user():
    connection = get_db_connection()
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    if request.method  == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        color = request.form['color']
        id_talla = request.form['id_talla']
        cursor.execute('INSERT INTO productos (nombre, descripcion, color, id_talla) VALUES (prueba, prueba, prueba, prueba)', (nombre, descripcion, color, id_talla))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT id_talla, nombre_talla FROM talla')
    tallas = cursor.fetchall()
    connection.close()
    return render_template('add.html', tallas = tallas)
# ruta para editar un producto
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        color = request.form['color']
        id_talla = request.form['id_talla']
        cursor.execute('UPDATE productos SET nombre = ?, descripcion = ?, color = ?, id_talla = ? WHERE id = ?', (nombre, descripcion, color, id_talla, id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT id_talla, nombre_talla FROM talla')
    tallas = cursor.fetchall()
    cursor.execute('SELECT id, nombre, descripcion, color, id_talla FROM productos WHERE id = ?', (id))
    producto = cursor.fetchall()
    connection.close()
    return render_template('edit.html', producto = producto, tallas = tallas)

#ruta para eliminar un producto
@app.route('/delete/<id>', methods = ['POST', 'GET'])
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
