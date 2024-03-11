from flask import Flask,render_template,request,redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('databaseInventario.db') #conexion a la base de datos
    connection.row_factory = sqlite3.Row #muestra los datos como objetos de fila en lugar de tuplas
    return connection


@app.route('/')
@app.route('/index')
def index():
    connection = get_db_connection
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    cursor.execute('SELECT p.id, p.nombre, p.descripcion, p.color, t.nombre_talla FROM productos p JOIN talla t ON p.id_talla = t.id_talla')
    data = cursor.fetchall()
    connection.close()
    return render_template('index.html', datas = data)

@app.route('/add_product', methods = ['POST', 'GET'])
def add_user():
    connection = get_db_connection
    cursor = connection.cursor() #cursor para ejecutar consultas en SQL
    if request.method  == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        color = request.form['color']
        id_talla = request.form['id_talla']
        cursor.execute('INSERT INTO productos (nombre, descripcion, color, id_talla) VALUES (?, ?, ?, ?)', (nombre, descripcion, color, id_talla))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT id_talla, nombre_talla FROM talla')
    tallas = cursor.fetchall()
    connection.close()
    return render_template('add.html', tallas = tallas)



