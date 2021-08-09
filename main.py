import psycopg2
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

from flaskext.mysql import MySQL

app = Flask(__name__,static_url_path='/static')

db=SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-34-232-191-133.compute-1.amazonaws.com",
    database="d8ig7998ra9rf5",
    user="czdfdojgmpjtll",
    password="3c86e4598bc481d607584a7a09d35e2bb8d3fc72edd7be93a44b2d567dd18537"
    )



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


        conenctar = conn.cursor()

        conenctar.execute("SELECT * from pedido")

        datos = conenctar.fetchall()

        print(datos)
        conenctar.close()

        return render_template('formulario.html', ver_pedido=datos)

@app.route("/guardar_pedido", methods=["POST"])
def guardar_pedido():

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    tipo = request.form["playera"]
    archivo = request.form["file"]
    descripcion = request.form["descripcion"]



    connectar = conn.cursor()

    connectar.execute("INSERT INTO Pedido(nombre, correo, Tipo, archivo, descripcion ) VALUES (%s,%s,%s,%s,%s)", (nombre, correo, tipo, archivo, descripcion, id))

    conn.commit()
    connectar.close()

    return redirect("/formulario")

@app.route("/eliminar_pedido/<string:id>")
def eliminar_pedido(id):

    connectar = conn.cursor()

    connectar.execute("DELETE FROM pedido where id_pedido={0}".format(id))

    conn.commit()
    connectar.close()

    return redirect("/formulario")

@app.route("/consultar_pedido/<id>")
def consultar_pedido(id):



    connectar = conn.cursor()

    connectar.execute("SELECT * FROM pedido where id_pedido = %s", (id))
    dato=connectar.fetchone()
    print(dato)
    conn.commit()
    connectar.close()

    return render_template("/editar_pedido.html", pedido=dato)

@app.route("/editar_pedido/<id>", methods=["post"])
def editar_pedido(id):

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    tipo = request.form["playera"]
    archivo = request.form["file"]
    descripcion = request.form["descripcion"]



    connectar = conn.cursor()

    connectar.execute("UPDATE pedido SET nombre=%s, correo=%s, Tipo=%s, archivo=%s, descripcion=%s where id_pedido=%s", (nombre, correo, tipo, archivo, descripcion, id))

    conn.commit()
    connectar.close()

    return redirect("/formulario")

if __name__ == '__main__':
    app.run(port = 3000,debug= True)