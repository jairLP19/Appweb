from flask import Flask,render_template, request ,url_for,redirect
from flaskext.mysql import MySQL



app = Flask(__name__,static_url_path='/static')

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Proyecto'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def info_html():
     return render_template('info.html')

@app.route("/index")
def index_html():
     return render_template('index.html')

@app.route("/formulario")
def formulario_html():

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * from pedido")

        datos = cursor.fetchall()

        print(datos)
        cursor.close()

        return render_template('formulario.html', ver_pedido=datos)

@app.route("/guardar_pedido", methods=["POST"])
def guardar_pedido():

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    tipo = request.form["playera"]
    archivo = request.form["file"]
    descripcion = request.form["descripcion"]

    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO Pedido(nombre, correo, Tipo, archivo, descripcion ) VALUES (%s,%s,%s,%s,%s)", (nombre, correo, tipo, archivo, descripcion, id))

    conn.commit()
    cursor.close()

    return redirect("/formulario")

@app.route("/eliminar_pedido/<string:id>")
def eliminar_pedido(id):

    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM pedido where id_pedido={0}".format(id))

    conn.commit()
    cursor.close()

    return redirect("/formulario")

@app.route("/consultar_pedido/<id>")
def consultar_pedido(id):

    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedido where id_pedido = %s", (id))
    dato=cursor.fetchone()
    print(dato)
    conn.commit()
    cursor.close()

    return render_template("/editar_pedido.html", pedido=dato)

@app.route("/editar_pedido/<id>", methods=["post"])
def editar_pedido(id):

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    tipo = request.form["playera"]
    archivo = request.form["file"]
    descripcion = request.form["descripcion"]

    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("UPDATE pedido SET nombre=%s, correo=%s, Tipo=%s, archivo=%s, descripcion=%s where id_pedido=%s", (nombre, correo, tipo, archivo, descripcion,id))

    conn.commit()
    cursor.close()

    return redirect("/formulario")

if __name__ == '__main__':
    app.run(port = 3000,debug= True)